import pandas as pd
import numpy as np

class Calc:
    def __init__(self):
        self.df = pd.read_csv(master)
        self.df["Issue Date"] = pd.to_datetime(self.df["Issue Date"], errors="coerce")
        self.df_compared = self.df.loc[self.df["Tenor"] != "28 DAYS"]
        self.df_compared.sort_values("Issue Date", inplace=True)
        self.df_compared.reset_index(drop=True, inplace=True)

        self.eth_tenor_91 = self.df_compared.loc[(self.df_compared["Tenor"] == "91 DAYS") & (self.df_compared["Country"] == "Ethiopia")]
        self.eth_tenor_182 = self.df_compared.loc[(self.df_compared["Tenor"] == "182 DAYS") & (self.df_compared["Country"] == "Ethiopia")]
        self.eth_tenor_364 = self.df_compared.loc[(self.df_compared["Tenor"] == "364 DAYS") & (self.df_compared["Country"] == "Ethiopia")]
        
        self.ksh_tenor_91 = self.df_compared.loc[(self.df_compared["Tenor"] == "91 DAYS") & (self.df_compared["Country"] == "Kenya")]
        self.ksh_tenor_182 = self.df_compared.loc[(self.df_compared["Tenor"] == "182 DAYS") & (self.df_compared["Country"] == "Kenya")]
        self.ksh_tenor_364 = self.df_compared.loc[(self.df_compared["Tenor"] == "364 DAYS") & (self.df_compared["Country"] == "Kenya")]

    

    def yield_spread(self):
            # Kenya - Ethiopia
        """ Ethiopia Monthly Yield"""
        eth_tenor_91 = self.eth_tenor_91[["Weighted Average Yield (Annual in %)", "Issue Date", "Total Amount Accepted (Millions)"]].copy()
        eth_tenor_91 = eth_tenor_91.dropna(subset=["Issue Date", "Weighted Average Yield (Annual in %)"])
        eth_tenor_91 = eth_tenor_91.set_index("Issue Date").sort_index()


        eth_tenor_182 = self.eth_tenor_182[["Weighted Average Yield (Annual in %)", "Issue Date", "Total Amount Accepted (Millions)"]].copy()
        eth_tenor_182 = eth_tenor_182.dropna(subset=["Issue Date", "Weighted Average Yield (Annual in %)"])
        eth_tenor_182 = eth_tenor_182.set_index("Issue Date").sort_index()


        eth_tenor_364 = self.eth_tenor_364[["Weighted Average Yield (Annual in %)", "Issue Date", "Total Amount Accepted (Millions)"]].copy()
        eth_tenor_364 = eth_tenor_364.dropna(subset=["Issue Date", "Weighted Average Yield (Annual in %)"])
        eth_tenor_364 = eth_tenor_364.set_index("Issue Date").sort_index()

        

        eth_y_91 = eth_tenor_91["Weighted Average Yield (Annual in %)"]
        eth_y_182 = eth_tenor_182["Weighted Average Yield (Annual in %)"]
        eth_y_364 = eth_tenor_364["Weighted Average Yield (Annual in %)"]
        
        
        eth_w_91 = eth_tenor_91["Total Amount Accepted (Millions)"]
        eth_w_182 = eth_tenor_182["Total Amount Accepted (Millions)"]
        eth_w_364 = eth_tenor_364["Total Amount Accepted (Millions)"]

        eth_monthly_91 = (
                            (eth_y_91 * eth_w_91).resample("ME").sum()
                               / 
                            eth_w_91.resample("ME").sum()
        )

        eth_monthly_182 = (
                            (eth_y_182 * eth_w_182).resample("ME").sum()
                               /
                            eth_w_182.resample("ME").sum()
        )

        eth_monthly_364 = (
                            (eth_y_364 * eth_w_364).resample("ME").sum()
                               /
                            eth_w_364.resample("ME").sum()
        )


        """ Kenya Monthly Yield"""
        ksh_tenor_91 = self.ksh_tenor_91[["Weighted Average Yield (Annual in %)", "Issue Date", "Total Amount Accepted (Millions)"]].copy()
        ksh_tenor_91 = ksh_tenor_91.dropna(subset=["Issue Date", "Weighted Average Yield (Annual in %)"])
        ksh_tenor_91 = ksh_tenor_91.set_index("Issue Date").sort_index()


        ksh_tenor_182 = self.ksh_tenor_182[["Weighted Average Yield (Annual in %)", "Issue Date", "Total Amount Accepted (Millions)"]].copy()
        ksh_tenor_182 = ksh_tenor_182.dropna(subset=["Issue Date", "Weighted Average Yield (Annual in %)"])
        ksh_tenor_182 = ksh_tenor_182.set_index("Issue Date").sort_index()


        ksh_tenor_364 = self.ksh_tenor_364[["Weighted Average Yield (Annual in %)", "Issue Date", "Total Amount Accepted (Millions)"]].copy()
        ksh_tenor_364 = ksh_tenor_364.dropna(subset=["Issue Date", "Weighted Average Yield (Annual in %)"])
        ksh_tenor_364 = ksh_tenor_364.set_index("Issue Date").sort_index()



        ksh_y_91 = ksh_tenor_91["Weighted Average Yield (Annual in %)"]
        ksh_y_182 = ksh_tenor_182["Weighted Average Yield (Annual in %)"]
        ksh_y_364 = ksh_tenor_364["Weighted Average Yield (Annual in %)"]


        ksh_w_91 = ksh_tenor_91["Total Amount Accepted (Millions)"]
        ksh_w_182 = ksh_tenor_182["Total Amount Accepted (Millions)"]
        ksh_w_364 = ksh_tenor_364["Total Amount Accepted (Millions)"]

        ksh_monthly_91 = (
                            (ksh_y_91 * ksh_w_91).resample("ME").sum()
                               /
                            ksh_w_91.resample("ME").sum()
        )

        ksh_monthly_182 = (
                            (ksh_y_182 * ksh_w_182).resample("ME").sum()
                               /
                            ksh_w_182.resample("ME").sum()
        )

        ksh_monthly_364 = (
                            (ksh_y_364 * ksh_w_364).resample("ME").sum()
                               /
                            ksh_w_364.resample("ME").sum()
        )
        spread_91 = ksh_monthly_91 - eth_monthly_91
        spread_182 = ksh_monthly_182 - eth_monthly_182
        spread_364 = ksh_monthly_364 - eth_monthly_364

        return spread_91, spread_182, spread_364
