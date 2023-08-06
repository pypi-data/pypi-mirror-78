from __future__ import annotations
from typing import Any, Dict, Iterable, Optional, Tuple, Union

import copy
import materia as mtr
from ..utils import memoize
import numpy as np
import scipy.integrate, scipy.interpolate

# import matplotlib.pyplot as plt
import warnings

# __all__ = []


class DataSeries:
    def __init__(self, x: mtr.Quantity, y: mtr.Quantity) -> None:
        self.x = x
        self.y = y

    # def plot(self):
    #     plt.plot(self.x.value, self.y.value)
    #     plt.show()


def broaden(
    self, fwhm: mtr.Quantity
) -> Callable[Iterable[Union[int, float]], Iterable[Union[int, float]]]:
    def f(energies: mtr.Quantity) -> Iterable[Union[int, float]]:
        s = 0
        # for excitation in self.excitations:
        #     x = (energies - excitation.energy) / fwhm
        #     x = np.array([e.value for e in x])
        #     s += excitation.oscillator_strength * np.exp(-np.log(2) * (2 * x ** 2))
        # return s
        for excitation in self.excitations:
            x = (energies - excitation.energy) / fwhm
            x = np.array([e.value for e in x])
            s += excitation.oscillator_strength * np.exp(-0.5 * x ** 2)
        return s / (np.sqrt(2 * np.pi) * fwhm)

    return f


def broaden(gamma):
    def _f(omega, gamma, w):
        return gamma * omega / ((w ** 2 - omega ** 2) ** 2 + omega ** 2 * gamma ** 2)

    def f(omega):
        return (fs[None, :] @ np.vstack([_f(omega, gamma, w) for w in ws])).squeeze()

    return f


class DeltaSeries:
    def __init__(self, x: mtr.Quantity, y: mtr.Quantity) -> None:
        self.x = x
        self.y = y / x.unit

    def broaden(self, peak_func, x_eval, in_place=True):
        value = peak_func(x=self.x, y=self.y, x_eval=x_eval)

        if in_place:
            self.x = x_eval * self.x.unit
            self.y = value * self.y.unit
            return self
        else:
            new_series = copy.deepcopy(self)
            new_series.x = x_eval * self.x.unit
            new_series.y = value * self.y.unit
            return new_series

    # def plot(self):
    #     plt.scatter(self.x.value, self.y.value)
    #     plt.show()


class TimeSeries(DataSeries):
    @property
    def dt(self) -> mtr.Quantity:
        # FIXME: should we even check for uniform spacing since this method,
        # like most/all methods, is susceptible to floating point errors?
        spacings = np.diff(self.x.value)
        dt, *_ = spacings
        if not np.allclose(spacings, dt):
            raise ValueError(
                "Time array does not have a unique spacing. Consider interpolating to a uniformly spaced time array first."
            )
        else:
            return dt * self.x.unit

    @property
    def T(self) -> mtr.Quantity:
        return self.x[-1] - self.x[0]

    def damp(self) -> None:  # , final_damp_value):
        final_damp_value = 1e-4  # Quantity(value=1e-4,unit=self.x.unit)
        etasq = -np.log(final_damp_value) / self.T ** 2

        damp = np.exp(-(etasq * self.x ** 2).value)

        self.y *= damp

    def fourier_transform(self, pad_len=None):
        if pad_len is None:
            pad_len = len(self.x)

        fft_value = np.fft.fft(a=self.y.value, n=pad_len) / pad_len
        fft_real = fft_value.real * self.y.unit
        fft_imag = fft_value.imag * self.y.unit
        fft_freq = np.fft.fftfreq(n=pad_len, d=self.dt().value) / self.x.unit

        return (
            mtr.Spectrum(x=fft_freq, y=fft_real),
            mtr.Spectrum(x=fft_freq, y=fft_imag),
        )
        # self.x,convert_from=self.x_store_unit,convert_to='second')
        # frequencies = scipy.fftpack.fftfreq(n=pad_len,d=self.dt())
        # self.x = self.converter.convert(quantity=self.x,convert_from='second',convert_to=self.x_store_unit)

        # return ComplexSpectrum(x_vals=2*np.pi*frequencies,x_unit='radian_per_second',y=fft,y_unit=self.y_store_unit)


class Spectrum(DataSeries):
    def match(self, match_to, in_place=True, interp_method="cubic_spline"):
        return self.extrapolate(x_extrap_to=match_to.x, in_place=in_place).interpolate(
            x_interp_to=match_to.x, in_place=in_place, method=interp_method
        )

    def extrapolate(self, x_extrap_to, in_place=True):
        if self.x.unit != x_extrap_to.unit:
            raise ValueError(
                "X-axis units do not match. Change units before extrapolating."
            )

        x_extrap, y_extrap = mtr.extrapolate(
            x=self.x.value, y=self.y.value, x_extrap_to=x_extrap_to.value
        )

        x_extrap = x_extrap * self.x.unit
        y_extrap = y_extrap * self.y.unit

        if in_place:
            self.x, self.y = x_extrap, y_extrap
            return self
        else:
            new_spectrum = copy.deepcopy(self)
            new_spectrum.x = x_extrap
            new_spectrum.y = y_extrap
            return new_spectrum
            # return self.__class__(x=x_extrap,y=y_extrap)

    def interpolate(self, x_interp_to, in_place=True, method="cubic_spline"):
        if self.x.unit != x_interp_to.unit:
            raise ValueError(
                "X-axis units do not match. Change units before interpolating."
            )

        x_interp, y_interp = mtr.interpolate(
            x=self.x.value, y=self.y.value, x_interp_to=x_interp_to.value, method=method
        )

        x_interp = x_interp * self.x.unit
        y_interp = y_interp * self.y.unit

        if in_place:
            self.x, self.y = x_interp, y_interp
            return self
        else:
            new_spectrum = copy.deepcopy(self)
            new_spectrum.x = x_interp
            new_spectrum.y = y_interp
            return new_spectrum
            # return self.__class__(x=x_interp, y=y_interp)

    # def plot(self, x=None):
    #     # FIXME: add axes labels, title
    #     if x is not None:
    #         plt.plot(x, self.y.match(match_to=x, in_place=False))
    #     else:
    #         plt.plot(self.x, self.y)
    #     plt.xlabel(f"Units: {self.x.unit}")
    #     plt.ylabel(f"Units: {self.y.unit}")
    #     plt.show()


class PolarizabilitySpectrum(Spectrum):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)


class AbsorptionSpectrum(Spectrum):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)


class ReflectanceSpectrum(Spectrum):
    def reflect_illuminant(self, illuminant):
        new_spectrum = copy.deepcopy(illuminant)
        new_spectrum.x = self.x
        new_spectrum.y = self.y * illuminant.match(match_to=self, in_place=False).y
        return new_spectrum


class TransmittanceSpectrum(Spectrum):
    def transmit_illuminant(self, illuminant):
        new_spectrum = copy.deepcopy(illuminant)
        new_spectrum.x = self.x
        new_spectrum.y = self.y * illuminant.match(match_to=self, in_place=False).y
        return new_spectrum

    def avt(self):
        from .data import ASTMG173

        photopic = PhotopicResponse().match(match_to=self)
        astmg = ASTMG173().match(match_to=self)
        num = scipy.integrate.simps(
            y=(self.y * astmg.y * photopic.y).value, x=self.x.value
        )
        denom = scipy.integrate.simps(y=(astmg.y * photopic.y).value, x=astmg.x.value)

        return num / denom


class SPDSpectrum(Spectrum):
    @property
    @memoize
    def XYZ(self) -> Tuple[float, float, float]:
        # FIXME: this is an ugly workaround to avoid circular import - change it!!
        from .data import (
            CIE1931ColorMatchingFunctionX,
            CIE1931ColorMatchingFunctionY,
            CIE1931ColorMatchingFunctionZ,
        )

        xbar = CIE1931ColorMatchingFunctionX().match(match_to=self, in_place=True)
        ybar = CIE1931ColorMatchingFunctionY().match(match_to=self, in_place=True)
        zbar = CIE1931ColorMatchingFunctionZ().match(match_to=self, in_place=True)

        X = scipy.integrate.simps(y=(self.y * xbar.y).value, x=self.x.value)
        Y = scipy.integrate.simps(y=(self.y * ybar.y).value, x=self.x.value)
        Z = scipy.integrate.simps(y=(self.y * zbar.y).value, x=self.x.value)

        return X / Y, 1.0, Z / Y

    # FIXME: verify correctness with test case
    def von_kries_XYZ(self, source_illuminant, destination_illuminant):
        source_lms = np.array(source_illuminant.LMS())
        destination_lms = np.array(destination_illuminant.LMS())
        LMS = np.array(self.LMS())[:, None]

        hpe = hunt_pointer_estevez_transform()
        adapted_LMS = np.diag(destination_lms / source_lms) @ LMS
        adapted_XYZ = np.linalg.inv(hpe) @ adapted_LMS

        adapted_X, adapted_Y, adapted_Z = adapted_XYZ.squeeze()

        return adapted_X, adapted_Y, adapted_Z

    def UVW(self, white_point=None):
        X, Y, Z = self.XYZ
        return self._XYZ_to_UVW(X=X, Y=Y, Z=Z, white_point=white_point)

    def von_kries_UVW(
        self, source_illuminant, destination_illuminant, white_point=None
    ):
        X, Y, Z = self.von_kries_XYZ(
            source_illuminant=source_illuminant,
            destination_illuminant=destination_illuminant,
        )

        return self._XYZ_to_UVW(X=X, Y=Y, Z=Z, white_point=white_point)
        # FIXME: shouldn't the white_point actually be the desination illuminant's white point?

    def _XYZ_to_UVW(self, X, Y, Z, white_point=None):
        if white_point is None:
            U = 2 * X / 3
            V = Y
            W = 0.5 * (-X + 3 * Y + Z)
        else:
            u0, v0 = white_point
            u, v = self.uv

            W = 25 * np.power(Y, 1 / 3) - 17
            U = 13 * W * (u - u0)
            V = 13 * W * (v - v0)

        return U, V, W

    @property
    def LMS(self):
        hpe = hunt_pointer_estevez_transform()

        XYZ = np.array((self.XYZ))[:, None]
        L, M, S = (hpe @ XYZ).squeeze()

        return L, M, S

    @property
    def xy(self) -> Tuple[float, float]:
        X, Y, Z = self.XYZ
        norm = sum(self.XYZ)

        x = X / norm
        y = Y / norm

        return x, y

    @property
    def uv(self) -> Tuple[float, float]:
        x, y = self.xy

        denom = -2 * x + 12 * y + 3

        u = 4 * x / denom
        v = 6 * y / denom

        return u, v

    # color properties

    @property
    def CCT_DC(self) -> Tuple[mtr.Quantity, float]:
        u, v = self.uv
        uvT = planckian_locus_ucs(exact=True)

        def _error(T):
            uT, vT = uvT(T=T)
            return (uT - u) ** 2 + (vT - v) ** 2

        CCT, DC_squared, _, _ = scipy.optimize.fminbound(
            func=_error, x1=1000, x2=15000, full_output=True
        )

        return CCT * mtr.K, np.sqrt(DC_squared)

    def cri(self, strict=True):
        # FIXME: this is an ugly workaround to avoid circular import - change it!!
        from .data import CIEIlluminantDSeries
        from .data import (
            CIE1995TestColorSample01,
            CIE1995TestColorSample02,
            CIE1995TestColorSample03,
            CIE1995TestColorSample04,
            CIE1995TestColorSample05,
            CIE1995TestColorSample06,
            CIE1995TestColorSample07,
            CIE1995TestColorSample08,
        )

        CCT, DC = self.CCT_DC

        if DC > 5.4e-3:
            if strict:
                raise ValueError(
                    "Distance from UCS Planckian locus too high. Illuminant is insufficiently white for accurate CRI determination."
                )
            else:
                warnings.warn(
                    "Distance from UCS Planckian locus too high. Illuminant is insufficiently white for accurate CRI determination."
                )

        if CCT < 5000 * mtr.K:
            from .data import BlackbodySPD

            reference_illuminant = BlackbodySPD(T=CCT, normalize_to=1)
        else:
            reference_illuminant = CIEIlluminantDSeries(T=CCT, normalize_to=1)

        samples = (
            CIE1995TestColorSample01(),
            CIE1995TestColorSample02(),
            CIE1995TestColorSample03(),
            CIE1995TestColorSample04(),
            CIE1995TestColorSample05(),
            CIE1995TestColorSample06(),
            CIE1995TestColorSample07(),
            CIE1995TestColorSample08(),
        )

        u_ref, v_ref = reference_illuminant.uv

        R_mean = np.mean(
            tuple(
                self.R_score(
                    test_illuminant=self,
                    reference_illuminant=reference_illuminant,
                    sample_reflectance=sample,
                )
                for sample in samples
            )
        )
        # (TCS01,TCS02,TCS03,TCS04,TCS05,TCS06,TCS07,TCS08)))

        return R_mean

    def R_score(self, test_illuminant, reference_illuminant, sample_reflectance):
        u_ref, v_ref = reference_illuminant.uv

        reflected_reference_illuminant = sample_reflectance.reflect_illuminant(
            reference_illuminant
        )
        u_sample_ref, v_sample_ref = reflected_reference_illuminant.uv

        _, reference_Y, _ = reference_illuminant.XYZ
        reflected_X, reflected_Y, reflected_Z = reflected_reference_illuminant.XYZ

        X_sample_ref = reflected_X * 100 / reference_Y
        Y_sample_ref = reflected_Y * 100 / reference_Y
        Z_sample_ref = reflected_Z * 100 / reference_Y
        U_ref, V_ref, W_ref = self._XYZ_to_UVW(
            X=X_sample_ref, Y=Y_sample_ref, Z=Z_sample_ref, white_point=(u_ref, v_ref)
        )

        reflected_test_illuminant = sample_reflectance.reflect_illuminant(
            illuminant=test_illuminant
        )
        u_sample_test, v_sample_test = reflected_test_illuminant.uv
        u_sample_adapted, v_sample_adapted = self.von_kries_uv(
            u=u_sample_test,
            v=v_sample_test,
            source_illuminant=test_illuminant,
            destination_illuminant=reference_illuminant,
        )

        _, test_Y, _ = test_illuminant.XYZ
        (
            reflected_test_X,
            reflected_test_Y,
            reflected_test_Z,
        ) = reflected_test_illuminant.XYZ

        X_sample_test = reflected_test_X * 100 / test_Y
        Y_sample_test = reflected_test_Y * 100 / test_Y
        Z_sample_test = reflected_test_Z * 100 / test_Y
        U_test, V_test, W_test = self._XYZ_to_UVW(
            X=X_sample_test,
            Y=Y_sample_test,
            Z=Z_sample_test,
            white_point=(u_ref, v_ref),
        )
        # FIXME: using the next three lines improves the answer for high temp blackbodies but they seem wrong...
        # W_test = 25*np.power(Y_sample_test,1/3) - 17
        # U_test = 13*W_test*(u_sample_adapted - u_ref)
        # V_test = 13*W_test*(v_sample_adapted - v_ref)

        distance = np.sqrt(
            (U_ref - U_test) ** 2 + (V_ref - V_test) ** 2 + (W_ref - W_test) ** 2
        )

        return 100 - 4.6 * distance

    def von_kries_uv(self, u, v, source_illuminant, destination_illuminant):
        u_s, v_s = source_illuminant.uv
        c_s = (4 - u_s - 10 * v_s) / v_s
        d_s = (1.708 * v_s + 0.404 - 1.481 * u_s) / v_s
        _, Y_s, _ = source_illuminant.XYZ

        u_d, v_d = destination_illuminant.uv
        c_d = (4 - u_d - 10 * v_d) / v_d
        d_d = (1.708 * v_d + 0.404 - 1.481 * u_d) / v_d
        _, Y_d, _ = destination_illuminant.XYZ

        c = (4 - u - 10 * v) / v
        d = (1.708 * v + 0.404 - 1.481 * u) / v

        denom = 16.518 + 1.481 * c_d * c / c_s - d_d * d / d_s
        u_adapted = (10.872 + 0.404 * c_d * c / c_s - 4 * d_d * d / d_s) / denom
        v_adapted = 5.520 / denom

        return u_adapted, v_adapted


class RelativeSPDSpectrum(SPDSpectrum):
    def __init__(self, x, y, normalizing_x=560, normalize_to=1):
        [
            val,
        ] = y[x.value == normalizing_x]

        super().__init__(
            x=x,
            y=normalize_to * y / val,
        )


def hunt_pointer_estevez_transform() -> np.ndarray:
    return np.array(
        [
            [0.4002400, 0.7076000, -0.0808100],
            [-0.2263000, 1.1653200, 0.0457000],
            [0.0000000, 0.0000000, 0.9182200],
        ]
    )


def planckian_locus_xyz(
    exact: Optional[bool] = False,
) -> Callable[mtr.Quantity, Tuple[float, float]]:
    if exact:
        # FIXME: this is an ugly workaround to avoid circular import - change it!!
        from .data import BlackbodySPD

        return lambda T: BlackbodySPD(T=T).xy
    else:

        def x(T):
            if T >= 1667 and T <= 4000:
                return (
                    -0.2661239e9 / T ** 3
                    - 0.2343589e6 / T ** 2
                    + 0.8776956e3 / T
                    + 0.179910
                )
            elif T > 4000 and T <= 25000:
                return (
                    -3.0258469e9 / T ** 3
                    + 2.1070379e6 / T ** 2
                    + 0.2226347e3 / T
                    + 0.240390
                )

        def y(T):
            xc = x(T)
            if T >= 1667 and T <= 2222:
                return (
                    -1.1063814 * xc ** 3
                    - 1.34811020 * xc ** 2
                    + 2.18555832 * xc
                    - 0.20219683
                )
            elif T > 2222 and T <= 4000:
                return (
                    -0.9549476 * xc ** 3
                    - 1.37418593 * xc ** 2
                    + 2.09137015 * xc
                    - 0.16748867
                )
            elif T > 4000 and T <= 25000:
                return (
                    3.0817580 * xc ** 3
                    - 5.87338670 * xc ** 2
                    + 3.75112997 * xc
                    - 0.37001483
                )

        return lambda T: (x(T=T), y(T=T))


def planckian_locus_ucs(
    exact: Optional[bool] = False,
) -> Callable[mtr.Quantity, Tuple[float, float]]:
    if exact:
        # FIXME: this is an ugly workaround to avoid circular import - change it!!
        from .data import BlackbodySPD

        return lambda T: BlackbodySPD(T=T).uv
    else:

        def f(T):
            u = (0.860117757 + 1.54118254e-4 * T + 1.28641212e-7 * T ** 2) / (
                1 + 8.42420235e-4 * T + 7.08145163e-7 * T ** 2
            )

            v = (0.317398726 + 4.22806245e-5 * T + 4.20481691e-8 * T ** 2) / (
                1 - 2.89741816e-5 * T + 1.61456053e-7 * T ** 2
            )

            return u, v

        return f


# standard illuminants, default normalized to 100 @ 560 nm


class PhotopicResponse(RelativeSPDSpectrum):
    def __init__(self):
        # data taken from https://web.archive.org/web/20170131100357/http://files.cie.co.at/204.xls
        x = np.linspace(380, 780, 81) * mtr.nm

        V = [
            0.000039,
            0.000064,
            0.000120,
            0.000217,
            0.000396,
            0.000640,
            0.001210,
            0.002180,
            0.004000,
            0.007300,
            0.011600,
            0.016840,
            0.023000,
            0.029800,
            0.038000,
            0.048000,
            0.060000,
            0.073900,
            0.090980,
            0.112600,
            0.139020,
            0.169300,
            0.208020,
            0.258600,
            0.323000,
            0.407300,
            0.503000,
            0.608200,
            0.710000,
            0.793200,
            0.862000,
            0.914850,
            0.954000,
            0.980300,
            0.994950,
            1.000000,
            0.995000,
            0.978600,
            0.952000,
            0.915400,
            0.870000,
            0.816300,
            0.757000,
            0.694900,
            0.631000,
            0.566800,
            0.503000,
            0.441200,
            0.381000,
            0.321000,
            0.265000,
            0.217000,
            0.175000,
            0.138200,
            0.107000,
            0.081600,
            0.061000,
            0.044580,
            0.032000,
            0.023200,
            0.017000,
            0.011920,
            0.008210,
            0.005723,
            0.004102,
            0.002929,
            0.002091,
            0.001484,
            0.001047,
            0.000740,
            0.000520,
            0.000361,
            0.000249,
            0.000172,
            0.000120,
            0.000085,
            0.000060,
            0.000042,
            0.000030,
            0.000021,
            0.000015,
        ]
        y = np.array(V) * mtr.unitless

        super().__init__(x=x, y=y, normalize_to=100)
