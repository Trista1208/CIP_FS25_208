import pandas as pd
import statsmodels.formula.api as smf



def load_old(old_csv = "robot_vacuums.csv", print_i = True):
    """
    Loads the original CSV file and returns it as a pandas DataFrame.
    
    Parameters:
        old_csv (str): Path to the CSV file containing raw product data.
        print_i (bool): If True, prints the percentage of missing values per column.
    
    Returns:
        pandas.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(old_csv)
    shape = df.shape
    if print_i:
        print(shape)
        for titel in df.keys():
            count_na = df[titel].isna().sum()
            print(f"{round(count_na * 100 / shape[0], 1)}% of {titel} are NA-values")
        return df


def load_new(new_csv = "robot_vacuums_cleaned.csv", print_i = True):
    """
    Loads the cleaned CSV file and returns it as a pandas DataFrame.
    
    Parameters:
        new_csv (str): Path to the cleaned CSV file.
        print_i (bool): If True, prints the percentage of missing values per column.
    
    Returns:
        pandas.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(new_csv)
    shape = df.shape
    if print_i:
        print(shape)
        for titel in df.keys():
            count_na = df[titel].isna().sum()
            print(f"{round(count_na * 100 / shape[0], 1)}% of {titel} are NA-values")
    return df


def inspecting_outputs(df):
    """
    Prints sample outputs from selected columns for inspection.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing robot vacuum product data.
    """
    [print(feature)for feature in df["features"][0:5]]
    print("\n")
    [print(feature)for feature in df["robot_type"][0:5]]
    print("\n")
    [print(feature)for feature in df["battery_life"][0:5]]
    print("\n")
    [print(feature)for feature in df["noise_level"][0:5]]
    print("\n")
    [print(feature)for feature in df["suction_power"][0:5]]
    print("\n")
    [print(feature)for feature in df["smart_home_ecosystem"][0:5]]
    

def onehot_encoding(df, print_i = True):
    """
    Applies one-hot encoding to the 'features' column and adds the new features to the DataFrame.
    Spaces and dashes in column names are replaced with underscores.
    
    Parameters:
        df (pandas.DataFrame): Input DataFrame with a 'features' column.
        print_i (bool): If True, prints the names of all resulting columns.
    
    Returns:
        pandas.DataFrame: Updated DataFrame with one-hot encoded features.
    """
    # if feature is Na, it should be detectable
    df["features_clean"] = df["features"].fillna("missing")
    onehot = df["features_clean"].str.get_dummies(sep="|")
    df_onehot = pd.concat([df, onehot], axis=1)
    # for some librarys it's not possible to work with these
    df_onehot.columns = df_onehot.columns.str.replace(" ", "_")
    df_onehot.columns = df_onehot.columns.str.replace("-", "_")

    if print_i:
        for titel in df_onehot.keys():
            print(f"{titel} + ", end="")
    
    return df_onehot


def price_efficiency(df, price_rel = 5, factor = 300, top = 10, print_sample = True):
    """
    Calculates a price-efficiency score for each product and prints the top products per category.

    Parameters:
        df (pandas.DataFrame): DataFrame containing product features and price.
        price_rel (float): Reduces the influence of price on the score (higher = less influence).
        factor (int): Multiplier to scale the final score to more readable values.
        top (int): Number of top products to display per robot type.
        print_sample (bool): If True, prints sample sizes per robot type.
    """
    if print_sample:
        print(df["robot_type"].value_counts(), "\n")

    for ro_type in df["robot_type"].unique()[:3]:
        df_filtered = df[df["robot_type"] == ro_type].copy()

        # make a quality score

        # get soome values important values at a quantile of 80%
        quantile = 0.8
        battery_qual = (df_filtered["battery_life"] / df_filtered["battery_life"].quantile(quantile)).clip(upper=1)
        noise_qual = (df_filtered["noise_level"] / df_filtered["noise_level"].quantile(quantile)).clip(upper=1)
        suction_qual = (df_filtered["suction_power"] / df_filtered["suction_power"].quantile(quantile)).clip(upper=1)
        room_qual = (df_filtered["room_area"] / df_filtered["room_area"].quantile(quantile)).clip(upper=1)

        # created a quality score over multiple value scores
        df_filtered["quality_score"] = pd.concat([battery_qual, noise_qual, suction_qual, room_qual], axis=1).mean(axis=1, skipna=True)

        # 300 are just because many prices are about 1000.- and a score from 0 - 100 is better to read than a verry small number
        # price ** 1/5 is to reduce the price influence on the result. Most good products are still verry cheap
        df_filtered["price_efficiency"] = df_filtered["quality_score"] / df_filtered["price"]**(1/5) * 300

        print(f"for the {ro_type} the ranking is:")
        
        top10 = df_filtered.sort_values("price_efficiency", ascending=False).head(top)
        print(top10[["product_name", "price_efficiency", "price"]].round(2))
        print("\n")
        

def feature_rating(df_onehot):
    """
    Runs a linear regression to analyze the influence of features on product ratings.
    Displays the features with the smallest p-values (most statistically significant).
    
    Parameters:
        df_onehot (pandas.DataFrame): One-hot encoded DataFrame with product features and ratings.
    """
    # ca. 200 left
    df_rating = df_onehot[df_onehot["rating_count"] >= 10]

    model = smf.ols(formula="rating ~ battery_life + noise_level + suction_power + room_area + Area_cleaning + Automatic_detergent_addition + Automatic_dust_emptying + Automatic_mop_pad_separation + Automatic_power_adjustment + Automatic_water_refill + Automatic_water_regulation + Base_station + Camera_function + Camera_based_navigation + Carpet_detection + Configurable_cleaning_programmes + Extendable_side_brushes + Extendable_wiping_pads + Fixed_water_connection + Independent_emptying + Infrared_sensor + Laser_navigation + Obstacle_detector + Programmable_cleaning_schedules + Programmable_room_boundary + Removable_water_tank + Self_cleaning_mop_pads + Staircase_safe", data=df_rating).fit()
    # Ergebnisse extrahieren
    results_df = pd.DataFrame({
        "coef": model.params,
        "std_err": model.bse,
        "t": model.tvalues,
        "p_value": model.pvalues
    })

    # Nach p-Wert sortieren
    sorted_results = results_df.sort_values("p_value")

    # Anzeigen
    print("top features with influence on the ratings with p < 0,1")
    print(sorted_results[sorted_results["p_value"] <= 0.1].round(3))
    

def price_efficiency_features(df_onehot, print_i = True):
    """
    Runs a linear regression to analyze the influence of features on product pricing.
    Filters extreme price outliers and shows the most statistically significant features.

    Parameters:
        df_onehot (pandas.DataFrame): One-hot encoded DataFrame with features and price.
        print_i (bool): If True, prints basic statistics and sample size before and after filtering.
    """
    if print_i:
        # ca 200 left
        df_price = df_onehot[df_onehot["rating_count"] >= 10]
        print("sample size before cleaning ", df_price.shape[0])
        print("price max ", df_price["price"].max())
        print("price mean ", df_price["price"].mean())
        print("price median ", df_price["price"].median())

        # there are some realy high price products, they are eliminated
        df_price = df_price[df_price["price"] <= 2000]
        print("sample size after cleaning ", df_price.shape[0])
        print("price mean ", df_price["price"].mean())
        print("price median ", df_price["price"].median())

    model = smf.ols(formula="price ~ battery_life + noise_level + suction_power + room_area + Area_cleaning + Automatic_detergent_addition + Automatic_dust_emptying + Automatic_mop_pad_separation + Automatic_power_adjustment + Automatic_water_refill + Automatic_water_regulation + Base_station + Camera_function + Camera_based_navigation + Carpet_detection + Configurable_cleaning_programmes + Extendable_side_brushes + Extendable_wiping_pads + Fixed_water_connection + Independent_emptying + Infrared_sensor + Laser_navigation + Obstacle_detector + Programmable_cleaning_schedules + Programmable_room_boundary + Removable_water_tank + Self_cleaning_mop_pads + Staircase_safe", data=df_price).fit()
    # Ergebnisse extrahieren
    results_df = pd.DataFrame({
        "coef": model.params,
        "std_err": model.bse,
        "t": model.tvalues,
        "p_value": model.pvalues
    })

    # Nach p-Wert sortieren
    sorted_results = results_df.sort_values("p_value")

    # Anzeigen
    print("top features with influence on the pricing with p < 0,1")
    print(sorted_results[sorted_results["p_value"] <= 0.1].round(3))