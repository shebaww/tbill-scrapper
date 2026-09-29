import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import numpy
from paths import data, results
import analysis
import pandas as pd

master = data / "master.csv"


class Illustrate:
    def __init__(self):
        self.Calc = analysis.Calc
        self.df = pd.read_csv(master)
        self.df["Issue Date"] = pd.to_datetime(self.df["Issue Date"], errors="coerce")
        self.df_compared = self.df.loc[self.df["Tenor"] != "28 DAYS"]
        self.df_compared.reset_index(drop=True, inplace=True)
        self.df_compared.sort_values("Issue Date", inplace=True)

        self.eth_tenor_91 = self.df_compared.loc[(self.df_compared["Tenor"] == "91 DAYS") & (self.df_compared["Country"] == "Ethiopia")]
        self.eth_tenor_182 = self.df_compared.loc[(self.df_compared["Tenor"] == "182 DAYS") & (self.df_compared["Country"] == "Ethiopia")]
        self.eth_tenor_364 = self.df_compared.loc[(self.df_compared["Tenor"] == "364 DAYS") & (self.df_compared["Country"] == "Ethiopia")]
        
        self.ksh_tenor_91 = self.df_compared.loc[(self.df_compared["Tenor"] == "91 DAYS") & (self.df_compared["Country"] == "Kenya")]
        self.ksh_tenor_182 = self.df_compared.loc[(self.df_compared["Tenor"] == "182 DAYS") & (self.df_compared["Country"] == "Kenya")]
        self.ksh_tenor_364 = self.df_compared.loc[(self.df_compared["Tenor"] == "364 DAYS") & (self.df_compared["Country"] == "Kenya")]

        
    
    def nominal_yield(self):
        tenor_colors = {"91 DAYS": "#1f77b4", "182 DAYS": "#ff7f0e", "364 DAYS": "#2ca02c"}
        tenor_ls = {"91 DAYS": "-", "182 DAYS": "--", "364 DAYS": "-."}
        tenors = ["91 DAYS", "182 DAYS", "364 DAYS"]

        fig, axes = plt.subplots(
            2, 1, figsize=(13, 8), sharex=True, sharey=True,
            gridspec_kw={"hspace": 0.12},
        )

        panels = [
            (axes[0], "Ethiopia",
             {"91 DAYS":  self.eth_tenor_91,
              "182 DAYS": self.eth_tenor_182,
              "364 DAYS": self.eth_tenor_364}),
            (axes[1], "Kenya",
             {"91 DAYS":  self.ksh_tenor_91,
              "182 DAYS": self.ksh_tenor_182,
              "364 DAYS": self.ksh_tenor_364}),
        ]

        for ax, country, by_tenor in panels:
            for tenor in tenors:
                d = by_tenor[tenor].copy()
                d["Issue Date"] = pd.to_datetime(d["Issue Date"], errors="coerce")
                d = d.dropna(subset=["Issue Date"]).sort_values("Issue Date")
                ax.plot(
                    d["Issue Date"],
                    d["Weighted Average Yield (Annual in %)"],
                    color=tenor_colors[tenor],
                    linewidth=1.6,
                    label=tenor.replace(" DAYS", "d"),
                    ls = tenor_ls[tenor]
                )

            ax.set_ylabel("Yield (%)", fontsize=10)
            ax1.set_xlabel("")
            ax2.set_xlabel("Issue Month", fontsize=10)
            ax.grid(True, alpha=0.25, linewidth=0.6)
            ax.set_axisbelow(True)
            ax.legend(
                title=country, loc="upper left", frameon=False,
                fontsize=9, title_fontsize=10,
            )
            ax.spines[["top", "right"]].set_visible(False)

        axes[1].xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
        axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.setp(axes[1].get_xticklabels(), rotation=0, ha="center")

        # tighten x to the data
        all_dates = pd.concat([
            pd.to_datetime(df["Issue Date"], errors="coerce")
            for panel in [self.eth_tenor_91, self.eth_tenor_182, self.eth_tenor_364,
                          self.ksh_tenor_91, self.ksh_tenor_182, self.ksh_tenor_364]
            for df in [panel]
        ]).dropna()
        axes[1].set_xlim(all_dates.min(), all_dates.max())

        plt.savefig(results / 'time-series-yield-curve.pdf', format="pdf", bbox_inches="tight")
        print("Saved to:", results / "time-series-yield-curve.pdf")


    
    def yield_spread(self):
        spread_91, spread_182, spread_364 = self.Calc.yield_spread(self)

        # ---- figure setup ----
        fig, ax = plt.subplots(figsize=(11, 6), dpi=150)

        colors = {
            "91d":  "#1f77b4",   # blue
            "182d": "#ff7f0e",   # orange
            "364d": "#2ca02c",   # green
        }

        for label, s, key, lsa in [
            ("91-day",  spread_91,  "91d", "-"),
            ("182-day", spread_182, "182d", "--"),
            ("364-day", spread_364, "364d", "-."),
        ]:
            ax.plot(
                s.index,
                s.to_numpy(),
                color=colors[key],
                linewidth=1.8,
                marker="o",
                markersize=3.5,
                markeredgewidth=0,
                label=f"{label} tenor",
                ls=lsa
            )

        # ---- reference line: zero spread ----
        ax.axhline(0, color="black", linewidth=0.9, linestyle="--", alpha=0.7)

        # ---- axes ----
        ax.set_xlabel("Issue month", fontsize=11)
        ax.set_ylabel("Yield Spread (Percentage Points)", fontsize=11)

        # ---- x-axis: quarterly ticks, no rotation, no phantom dates ----
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.tick_params(axis="x", which="major", length=5)
        ax.tick_params(axis="x", which="minor", length=2, color="#bbbbbb")

        # ---- y-axis: tighter, cleaner ----
        ax.yaxis.set_major_locator(MultipleLocator(2.5))
        ax.tick_params(axis="y", labelsize=10)

        # ---- grid & spines ----
        ax.grid(True, which="major", axis="y", alpha=0.25, linewidth=0.6)
        ax.grid(True, which="major", axis="x", alpha=0.15, linewidth=0.6)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color("#888888")
        ax.spines["bottom"].set_color("#888888")

        # ---- legend ----
        leg = ax.legend(
            loc="lower right",
            frameon=True,
            framealpha=0.95,
            edgecolor="#dddddd",
            fontsize=10,
            title="Spread by tenor",
            title_fontsize=10,
        )
        leg.get_frame().set_linewidth(0.6)

        fig.tight_layout(rect=[0, 0.02, 1, 1])

        # ---- save as vector PDF ----
        fig.savefig( data / results / "yield_spread_ke_et.pdf", bbox_inches="tight")
        print("Saved to:", data / results / "yield_spread_ke_et.pdf")
        plt.close(fig)     # don't call plt.show() after saving in a script





def main():
    illustrate = Illustrate()
    illustrate.yield_spread()
    illustrate.nominal_yield()

if __name__ == "__main__":
    main()





def main():
    illustrate = Illustrate()
    illustrate.yield_spread()

if __name__ == "__main__":
    main()
