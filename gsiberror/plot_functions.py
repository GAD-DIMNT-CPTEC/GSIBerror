#! /usr/bin/env python3

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# This function defines the names of the variables and mnemonics
def var_name(var):
    variables = {
        "sf": ("Stream function", r"$\psi$"),
        "vp": ("Velocity Potential", r"$\chi$"),
        "t": ("Virtual Temperature", "$tv$"),
        "q": ("Pseudo-Relative Humidity - qoption=1", "$rh_{p}$"),
        "qin": ("Normalized Relative Humidity - qoption=2", "$rh_{n}$"),
        "oz": ("Ozone", "$oz$"),
        "ps": ("Surface Pressure", "$ps$"),
        "cw": ("Liquid Cloud Water Content", "$cw$"),
        "sst": ("Sea Surface Temperature", "$sst$"),
    }
    try:
        return variables[var]
    except KeyError as exc:
        raise ValueError(
            f"Unknown variable {var!r}; expected one of {', '.join(variables)}"
        ) from exc


# This function defines global values of min and max given two xarrays
def global_minmax(l_matrix, t_array, m_rec, scale=1.0):

    if not l_matrix:
        raise ValueError("At least one Berror matrix is required")
    if t_array not in {"balprojs", "amplitudes", "hscales", "vscales"}:
        raise ValueError(f"Unknown data collection {t_array!r}")

    lmin = []
    lmax = []

    for mtx in l_matrix:
        values = getattr(mtx, t_array)[str(m_rec)] * scale
        vmin = float(values.min())
        vmax = float(values.max())

        lmin.append(vmin)
        lmax.append(vmax)

    return min(lmin), max(lmax)


# This function plots the regression coefficients
def plot_reg_coeffs(lmatrix, rec, lev, **kwargs):
    if not lmatrix:
        raise ValueError("At least one Berror matrix is required")
    if rec not in {"agvin", "bgvin", "wgvin"}:
        raise ValueError("rec must be one of 'agvin', 'bgvin', or 'wgvin'")

    if "eqrange" in kwargs:
        eqrange = kwargs["eqrange"]
    else:
        eqrange = False

    if "suptitle" in kwargs:
        suptitle = kwargs["suptitle"]
    else:
        suptitle = False

    if "savefig" in kwargs:
        savefig = kwargs["savefig"]
    else:
        savefig = False

    len_lmatrix = len(lmatrix)

    if eqrange:
        scale = 1e2 if rec == "wgvin" else 1.0
        minval, maxval = global_minmax(lmatrix, "balprojs", str(rec), scale)

    length_x_axis = 20
    length_y_axis = 10
    fig_height = 5.0

    rows = 1
    columns = len_lmatrix

    height = length_y_axis * rows
    width = length_x_axis * columns

    plot_aspect_ratio = float(width) / float(height)

    fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    spec = fig.add_gridspec(ncols=len_lmatrix, nrows=rows, wspace=0.25, hspace=0.25)

    cbar_kwargs = {
        "spacing": "proportional",
        "pad": 0.08,
        "shrink": 1,
        "aspect": 15,
        "extend": "neither",
    }

    for i in range(rows * columns):
        ax = fig.add_subplot(spec[i])

        if rec == "agvin":
            nrec = "Virtual Temperature"
            if eqrange:
                lmatrix[i].balprojs[str(rec)].isel(level_2=lev).plot.contourf(
                    vmin=minval,
                    vmax=maxval,
                    add_colorbar=True,
                    cbar_kwargs=cbar_kwargs,
                    ax=ax,
                )
            else:
                lmatrix[i].balprojs[str(rec)].isel(level_2=lev).plot.contourf(
                    add_colorbar=True, cbar_kwargs=cbar_kwargs, ax=ax
                )
        elif rec == "bgvin":
            nrec = "Velocity Potencial"
            if eqrange:
                lmatrix[i].balprojs[str(rec)].plot.contourf(
                    vmin=minval,
                    vmax=maxval,
                    add_colorbar=True,
                    cbar_kwargs=cbar_kwargs,
                    ax=ax,
                )
            else:
                lmatrix[i].balprojs[str(rec)].plot.contourf(
                    add_colorbar=True, cbar_kwargs=cbar_kwargs, ax=ax
                )
        elif rec == "wgvin":
            nrec = "Surface Pressure"
            # Note: multiplying by 1e2 (100) to make it comparable to https://dtcenter.ucar.edu/com-GSI/users/docs/presentations/2011_tutorial/L8_06302011-BkgObsErrs-DarylKleist.pdf
            wgproj = lmatrix[i].balprojs[str(rec)] * 1e2
            if eqrange:
                wgproj.isel(level=0, latitude=slice(0, -2)).plot.line(
                    ylim=[minval, maxval], ax=ax
                )
            else:
                wgproj.isel(level=0, latitude=slice(0, -2)).plot.line(ax=ax)

        ax.set_title(
            str(lmatrix[i].get_name()) + "\n" + str(lmatrix[i].nlev) + " levels"
        )

        if suptitle:
            if rec == "agvin":
                sptitle = plt.suptitle(
                    r"Projection of the Stream Function ($\psi$) at the level "
                    + str(lev)
                    + " over the vertical profile of the balanced part of "
                    + str(nrec)
                    + r" ($\mathbf{G}_{"
                    + str(lev)
                    + r"}$): $T_{b}=\mathbf{G}\psi$",
                    y=1.05,
                    fontsize=16,
                )
            elif rec == "bgvin":
                sptitle = plt.suptitle(
                    r"Projection of the Stream Function ($\psi$) over the balanced part of "
                    + str(nrec)
                    + r" ($\mathbf{c}$): $\chi_{b}=\mathbf{c}\psi$",
                    y=1.05,
                    fontsize=16,
                )
            elif rec == "wgvin":
                sptitle = plt.suptitle(
                    r"Projection of the Stream Function of the Stream Function ($\psi$) over the balanced part of "
                    + str(nrec)
                    + r" ($\mathbf{w}$): $ps_{b}=\mathbf{w}\psi$",
                    y=1.05,
                    fontsize=16,
                )

    if savefig:
        if suptitle:
            fig.savefig(
                "reg_coeffs_" + str(rec) + ".png",
                dpi=fig.dpi,
                bbox_inches="tight",
                bbox_extra_artists=[sptitle],
            )
        else:
            fig.savefig(
                "reg_coeffs_" + str(rec) + ".png", dpi=fig.dpi, bbox_inches="tight"
            )

    return fig


# This function plots the amplitudes
def plot_amplitudes(lmatrix, rec, **kwargs):
    if not lmatrix:
        raise ValueError("At least one Berror matrix is required")
    var_name(rec)

    if "eqrange" in kwargs:
        eqrange = kwargs["eqrange"]
    else:
        eqrange = False

    if "profile" in kwargs:
        profile = kwargs["profile"]
    else:
        profile = False

    if "suptitle" in kwargs:
        suptitle = kwargs["suptitle"]
    else:
        suptitle = False

    if "savefig" in kwargs:
        savefig = kwargs["savefig"]
    else:
        savefig = False

    if rec == "ps" or rec == "sst":
        profile = False

    len_lmatrix = len(lmatrix)

    if eqrange:
        scale = 1e2 if rec in {"q", "qin"} and not profile else 1.0
        minval, maxval = global_minmax(lmatrix, "amplitudes", str(rec), scale)

    length_x_axis = 20
    length_y_axis = 10
    fig_height = 5.0

    rows = 1
    columns = len_lmatrix

    height = length_y_axis * rows
    width = length_x_axis * columns

    plot_aspect_ratio = float(width) / float(height)

    fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    #    if profile:
    #        fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))
    #    else:
    #        if rec == 'sst':
    #            fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))
    #        else:
    #            fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    spec = fig.add_gridspec(ncols=len_lmatrix, nrows=rows, wspace=0.25, hspace=0.25)

    cbar_kwargs = {
        "spacing": "proportional",
        "pad": 0.08,
        "shrink": 1,
        "aspect": 15,
        "extend": "neither",
    }

    crs = ccrs.PlateCarree()

    nrec = var_name(rec)[0]
    srec = var_name(rec)[1]

    for i in range(rows * columns):
        if rec == "sst":
            ax = plt.subplot(spec[i], projection=crs)
        else:
            ax = plt.subplot(spec[i])

        if profile:
            if eqrange:
                lmatrix[i].amplitudes[str(rec)].mean(dim="latitude").plot(
                    ax=ax, y="level", xlim=(minval, maxval)
                )
            else:
                lmatrix[i].amplitudes[str(rec)].mean(dim="latitude").plot(
                    ax=ax, y="level"
                )
        else:
            if rec == "sst":
                plot_kwargs = {"vmin": minval, "vmax": maxval} if eqrange else {}
                lmatrix[i].amplitudes[str(rec)].plot.contourf(
                    ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs, **plot_kwargs
                )
                ax.add_feature(
                    cfeature.NaturalEarthFeature(
                        "physical", "land", "110m", edgecolor="face", facecolor="white"
                    )
                )
                ax.coastlines()
            elif rec == "qin":
                # Note 1: slice(0,25) is applied to plot just the first quarter of the field
                #         in an attempt to retrieve something comparable to https://dtcenter.ucar.edu/com-GSI/users/docs/presentations/2011_tutorial/L8_06302011-BkgObsErrs-DarylKleist.pdf
                # Note 2: multiplying by 1e2 (100) to make it comparable to the above document
                ampqin = lmatrix[i].amplitudes[str(rec)] * 1e2
                if eqrange:
                    ampqin.isel(latitude=slice(0, 25)).drop("latitude").plot.contourf(
                        ax=ax,
                        vmin=minval,
                        vmax=maxval,
                        add_colorbar=True,
                        cbar_kwargs=cbar_kwargs,
                        add_labels=False,
                    )
                else:
                    ampqin.isel(latitude=slice(0, 25)).drop("latitude").plot.contourf(
                        ax=ax,
                        add_colorbar=True,
                        cbar_kwargs=cbar_kwargs,
                        add_labels=False,
                    )
            elif rec == "q":
                # Note: multiplying by 1e2 (100) to make it comparable to the above document
                ampq = lmatrix[i].amplitudes[str(rec)] * 1e2
                if eqrange:
                    ampq.plot.contourf(
                        ax=ax,
                        vmin=minval,
                        vmax=maxval,
                        add_colorbar=True,
                        cbar_kwargs=cbar_kwargs,
                    )
                else:
                    ampq.plot.contourf(
                        ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs
                    )
            elif rec == "ps":
                if eqrange:
                    lmatrix[i].amplitudes[str(rec)].plot(ax=ax, ylim=(minval, maxval))
                else:
                    # im = lmatrix[i].amplitudes[str(rec)].plot(ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs)
                    lmatrix[i].amplitudes[str(rec)].plot(ax=ax)
            else:
                if eqrange:
                    lmatrix[i].amplitudes[str(rec)].plot.contourf(
                        ax=ax,
                        vmin=minval,
                        vmax=maxval,
                        add_colorbar=True,
                        cbar_kwargs=cbar_kwargs,
                    )
                else:
                    lmatrix[i].amplitudes[str(rec)].plot.contourf(
                        ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs
                    )

        if rec == "sst":
            ax.set_title(str(lmatrix[i].get_name()))
        else:
            ax.set_title(
                str(lmatrix[i].get_name()) + " (" + str(lmatrix[i].nlev) + " levels)"
            )

        if suptitle:
            if rec == "sf":
                sptitle = plt.suptitle(
                    "Standard Deviation of " + str(nrec) + " (" + str(srec) + ")",
                    y=1.05,
                    fontsize=16,
                )
            elif rec == "q" or rec == "qin":
                sptitle = plt.suptitle(
                    "Standard Deviation of the unbalanced part of "
                    + str(nrec)
                    + " ("
                    + str(srec)
                    + ", %)",
                    y=1.05,
                )
            else:
                # sptitle = plt.suptitle('Desvio Padrão da Parte não balanceada da ' + str(nrec) + ' (' + str(srec) + ')', y=1.05)
                sptitle = plt.suptitle(
                    "Standard Deviation of the unbalanced part of "
                    + str(nrec)
                    + " ("
                    + str(srec)
                    + ")",
                    y=1.05,
                )

    if savefig:
        if suptitle:
            fig.savefig(
                "amplitudes_" + str(rec) + ".png",
                dpi=fig.dpi,
                bbox_inches="tight",
                bbox_extra_artists=[sptitle],
            )
        else:
            fig.savefig(
                "amplitudes_" + str(rec) + ".png", dpi=fig.dpi, bbox_inches="tight"
            )

    return fig


# This function plots the horizontal length scales
def plot_hscales(lmatrix, rec, **kwargs):
    if not lmatrix:
        raise ValueError("At least one Berror matrix is required")
    var_name(rec)

    if "eqrange" in kwargs:
        eqrange = kwargs["eqrange"]
    else:
        eqrange = False

    if "suptitle" in kwargs:
        suptitle = kwargs["suptitle"]
    else:
        suptitle = False

    if "savefig" in kwargs:
        savefig = kwargs["savefig"]
    else:
        savefig = False

    len_lmatrix = len(lmatrix)

    if eqrange:
        minval, maxval = global_minmax(lmatrix, "hscales", str(rec), 1e-3)

    #    if rec == 'sst':
    #        fig, axs = plt.subplots(1, len_lmatrix, constrained_layout=False, figsize=(20,4), subplot_kw={'projection': ccrs.PlateCarree()})
    #    else:
    #        fig, axs = plt.subplots(1, len_lmatrix, constrained_layout=False, figsize=(10,4))

    length_x_axis = 20
    length_y_axis = 10
    fig_height = 5.0

    rows = 1
    columns = len_lmatrix

    height = length_y_axis * rows
    width = length_x_axis * columns

    plot_aspect_ratio = float(width) / float(height)

    fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    #    if rec == 'sst':
    #        fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))
    #    else:
    #        fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    spec = fig.add_gridspec(ncols=len_lmatrix, nrows=rows, wspace=0.25, hspace=0.25)

    cbar_kwargs = {
        "spacing": "proportional",
        "pad": 0.08,
        "shrink": 1,
        "aspect": 15,
        "extend": "neither",
    }

    crs = ccrs.PlateCarree()

    nrec = var_name(rec)[0]
    srec = var_name(rec)[1]

    for i in range(rows * columns):
        if rec == "sst":
            ax = plt.subplot(spec[i], projection=crs)
        else:
            ax = plt.subplot(spec[i])

        # m -> km to make it consistent with https://dtcenter.ucar.edu/com-GSI/users/docs/presentations/2011_tutorial/L8_06302011-BkgObsErrs-DarylKleist.pdf
        hscl = lmatrix[i].hscales[str(rec)] * 1e-3

        if rec == "sst":
            plot_kwargs = {"vmin": minval, "vmax": maxval} if eqrange else {}
            hscl.plot.contourf(
                ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs, **plot_kwargs
            )
            ax.add_feature(
                cfeature.NaturalEarthFeature(
                    "physical", "land", "110m", edgecolor="face", facecolor="white"
                )
            )
            ax.coastlines()

        elif rec == "ps":
            if eqrange:
                hscl.plot(ax=ax, ylim=(minval, maxval))
            else:
                hscl.plot(ax=ax)  # , add_colorbar=True, cbar_kwargs=cbar_kwargs)
        else:
            if eqrange:
                hscl.plot.contourf(
                    ax=ax,
                    vmin=minval,
                    vmax=maxval,
                    add_colorbar=True,
                    cbar_kwargs=cbar_kwargs,
                )
            else:
                hscl.plot.contourf(ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs)

        if rec == "sst":
            ax.set_title(str(lmatrix[i].get_name()))
        else:
            ax.set_title(
                str(lmatrix[i].get_name()) + " (" + str(lmatrix[i].nlev) + " levels)"
            )

        if suptitle:
            sptitle = plt.suptitle(
                "Horizontal Length Scale of " + str(nrec) + " (" + str(srec) + ", km)",
                y=1.05,
                fontsize=16,
            )

    if savefig:
        if suptitle:
            fig.savefig(
                "hscales_" + str(rec) + ".png",
                dpi=fig.dpi,
                bbox_inches="tight",
                bbox_extra_artists=[sptitle],
            )
        else:
            fig.savefig(
                "hscales_" + str(rec) + ".png", dpi=fig.dpi, bbox_inches="tight"
            )

    return fig


# This function plots vertical length scales
def plot_vscales(lmatrix, rec, **kwargs):
    if not lmatrix:
        raise ValueError("At least one Berror matrix is required")
    var_name(rec)

    if "eqrange" in kwargs:
        eqrange = kwargs["eqrange"]
    else:
        eqrange = False

    if "suptitle" in kwargs:
        suptitle = kwargs["suptitle"]
    else:
        suptitle = False

    if "savefig" in kwargs:
        savefig = kwargs["savefig"]
    else:
        savefig = False

    len_lmatrix = len(lmatrix)

    if eqrange:
        minval, maxval = global_minmax(lmatrix, "vscales", str(rec))

    #    if rec == 'sst':
    #        fig, axs = plt.subplots(1, len_lmatrix, constrained_layout=False, figsize=(20,4), subplot_kw={'projection': ccrs.PlateCarree()})
    #    else:
    #        fig, axs = plt.subplots(1, len_lmatrix, constrained_layout=False, figsize=(10,4))

    length_x_axis = 20
    length_y_axis = 10
    fig_height = 5.0

    rows = 1
    columns = len_lmatrix

    height = length_y_axis * rows
    width = length_x_axis * columns

    plot_aspect_ratio = float(width) / float(height)

    #    if rec == 'sst':
    #        fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))
    #    else:
    #        fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    fig = plt.figure(figsize=(fig_height * plot_aspect_ratio, fig_height))

    spec = fig.add_gridspec(ncols=len_lmatrix, nrows=rows, wspace=0.25, hspace=0.25)

    cbar_kwargs = {
        "spacing": "proportional",
        "pad": 0.08,
        "shrink": 1,
        "aspect": 15,
        "extend": "neither",
    }

    nrec = var_name(rec)[0]
    srec = var_name(rec)[1]

    for i in range(rows * columns):
        ax = plt.subplot(spec[i])

        if eqrange:
            lmatrix[i].vscales[str(rec)].plot.contourf(
                ax=ax,
                vmin=minval,
                vmax=maxval,
                add_colorbar=True,
                cbar_kwargs=cbar_kwargs,
            )
        else:
            lmatrix[i].vscales[str(rec)].plot.contourf(
                ax=ax, add_colorbar=True, cbar_kwargs=cbar_kwargs
            )

        ax.set_title(
            str(lmatrix[i].get_name()) + " (" + str(lmatrix[i].nlev) + " levels)"
        )

        if suptitle:
            sptitle = plt.suptitle(
                "Vertical Length Scale of "
                + str(nrec)
                + " ("
                + str(srec)
                + ", grid units)",
                y=1.05,
                fontsize=16,
            )

    if savefig:
        if suptitle:
            fig.savefig(
                "vscales_" + str(rec) + ".png",
                dpi=fig.dpi,
                bbox_inches="tight",
                bbox_extra_artists=[sptitle],
            )
        else:
            fig.savefig(
                "vscales_" + str(rec) + ".png", dpi=fig.dpi, bbox_inches="tight"
            )

    return fig
