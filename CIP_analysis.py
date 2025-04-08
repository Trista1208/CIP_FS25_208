import pandas as pd
import statsmodels.formula.api as smf
import numpy as np



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
    Applies one-hot encoding to the 'features' column and adds the resulting features to the DataFrame.
    Spaces and dashes in column names are replaced with underscores.

    Parameters:
        df (pandas.DataFrame): Input DataFrame with a 'features' column.
        print_i (bool): If True, prints the names of all resulting columns.

    Returns:
        pandas.DataFrame: Updated DataFrame with one-hot encoded features.
    """
    # If a feature is NaN, it should be labeled as "missing"
    df["features_clean"] = df["features"].fillna("missing")
    onehot = df["features_clean"].str.get_dummies(sep="|")
    df_onehot = pd.concat([df, onehot], axis=1)
    # Some libraries don't work well with spaces or dashes in column names
    df_onehot.columns = df_onehot.columns.str.replace(" ", "_")
    df_onehot.columns = df_onehot.columns.str.replace("-", "_")

    if print_i:
        for titel in df_onehot.keys():
            print(f"{titel} + ", end="")
    
    return df_onehot


def price_efficiency(df, price_rel = 5, factor = 300, top = 10, quantile = 0.8, print_sample = True):
    """
    Calculates a price-efficiency score for each product and prints the top products per category.

    Parameters:
        df (pandas.DataFrame): DataFrame containing product features and price.
        price_rel (float): Reduces the influence of price on the score (higher = less influence).
        factor (int): Multiplier to scale the final score to more readable values.
        top (int): Number of top products to display per robot type.
        print_sample (bool): If True, prints sample sizes per robot type.
    """
    # Get information about robot types
    if print_sample:
        print("Info to the types:")
        print(df["robot_type"].value_counts(), "\n")

    for ro_type in df["robot_type"].unique()[:3]:
        df_filtered = df[df["robot_type"] == ro_type].copy()

        # Calculate quality score based on selected features

        # Extract feature quality at a given quantile (e.g., 80%)
        battery_qual = (df_filtered["battery_life"] / df_filtered["battery_life"].quantile(quantile)).clip(upper=1)
        noise_qual = (df_filtered["noise_level"] / df_filtered["noise_level"].quantile(quantile)).clip(upper=1)
        suction_qual = (df_filtered["suction_power"] / df_filtered["suction_power"].quantile(quantile)).clip(upper=1)
        room_qual = (df_filtered["room_area"] / df_filtered["room_area"].quantile(quantile)).clip(upper=1)

        # Create a combined quality score from multiple features
        df_filtered["quality_score"] = pd.concat([battery_qual, noise_qual, suction_qual, room_qual], axis=1).mean(axis=1, skipna=True)

        # Scaling by 300 makes the score more readable (since prices are often >1000)
        # price ** (1/price_rel) reduces the influence of price on the score
        df_filtered["price_efficiency"] = df_filtered["quality_score"] / df_filtered["price"]**(1/price_rel) * factor
        # Print the top-ranked products for the current robot type
        print(f"For the '{ro_type}' the ranking is:")
        
        top10 = df_filtered.sort_values("price_efficiency", ascending=False).head(top)
        print(top10[["product_name", "price_efficiency", "price"]].round(2))
        print("\n\n\n")
        

def feature_rating(df_onehot):
    """
    Runs a linear regression to analyze the influence of features on product ratings.
    Displays the features with the smallest p-values (most statistically significant).

    Parameters:
        df_onehot (pandas.DataFrame): One-hot encoded DataFrame with product features and ratings.
    """
    # Filter to products with a reasonable number of ratings (e.g., 10+)
    # ca. 200 left
    df_rating = df_onehot[df_onehot["rating_count"] >= 10]

    model = smf.ols(formula="rating ~ battery_life + noise_level + suction_power + room_area + Area_cleaning + Automatic_detergent_addition + Automatic_dust_emptying + Automatic_mop_pad_separation + Automatic_power_adjustment + Automatic_water_refill + Automatic_water_regulation + Base_station + Camera_function + Camera_based_navigation + Carpet_detection + Configurable_cleaning_programmes + Extendable_side_brushes + Extendable_wiping_pads + Fixed_water_connection + Independent_emptying + Infrared_sensor + Laser_navigation + Obstacle_detector + Programmable_cleaning_schedules + Programmable_room_boundary + Removable_water_tank + Self_cleaning_mop_pads + Staircase_safe", data=df_rating).fit()
    # Extract regression results
    results_df = pd.DataFrame({
        "coef": model.params,
        "std_err": model.bse,
        "t": model.tvalues,
        "p_value": model.pvalues
    })

    # Sort by p-value to find the most significant features
    sorted_results = results_df.sort_values("p_value")

    # Display only features with p-values < 0.1
    print("Top features with influence on the ratings with p < 0,1")
    print(sorted_results[sorted_results["p_value"] <= 0.1].round(3))
    print("\n\n\n")
    

def price_efficiency_features(df_onehot, print_i = True):
    """
    Runs a linear regression to analyze the influence of features on product pricing.
    Filters extreme price outliers and shows the most statistically significant features.

    Parameters:
        df_onehot (pandas.DataFrame): One-hot encoded DataFrame with features and price.
        print_i (bool): If True, prints basic statistics and sample size before and after filtering.
    """
    # Filter to products with sufficient rating count
    # Display price statistics before filtering
    # ca 200 left
    df_price = df_onehot[df_onehot["rating_count"] >= 10]
    if print_i:
        print("Info to the cleaning:")
        print("sample size before cleaning ", df_price.shape[0])
        print("price max ", df_price["price"].max())
        print("price mean ", df_price["price"].mean())
        print("price median ", df_price["price"].median())

    # Remove outliers with very high prices (> 2000)
    df_price = df_price[df_price["price"] <= 2000]
    if print_i:
        print("sample size after cleaning ", df_price.shape[0])
        print("price mean ", df_price["price"].mean())
        print("price median ", df_price["price"].median())
        print("\n")
    
    # Define the formula using selected features
    formula = (
    "battery_life + noise_level + suction_power + room_area + "
    "Area_cleaning + Automatic_detergent_addition + Automatic_dust_emptying + "
    "Automatic_mop_pad_separation + Automatic_power_adjustment + Automatic_water_refill + "
    "Automatic_water_regulation + Base_station + Camera_function + Camera_based_navigation + "
    "Carpet_detection + Configurable_cleaning_programmes + Extendable_side_brushes + "
    "Extendable_wiping_pads + Fixed_water_connection + Independent_emptying + "
    "Infrared_sensor + Laser_navigation + Obstacle_detector + Programmable_cleaning_schedules + "
    "Programmable_room_boundary + Removable_water_tank + Self_cleaning_mop_pads + Staircase_safe")

    # Run linear regression for price
    model_price = smf.ols(formula=f"price ~ {formula}", data=df_price).fit()
    results_price = pd.DataFrame({
        "coef_price": model_price.params,
        "p_price": model_price.pvalues})

    # Run linear regression for rating
    model_rating = smf.ols(formula=f"rating ~ {formula}", data=df_price).fit()
    results_rating = pd.DataFrame({
        "coef_rating": model_rating.params,
        "p_rating": model_rating.pvalues})

    # Join price and rating results and drop the intercept
    results = results_price.join(results_rating, how="inner")
    results = results.drop(index="Intercept")

    # Calculate influence scores based on coefficients and p-values
    results["score_price"] = - results["coef_price"] * -np.log10(results["p_price"])
    results["score_rating"] = results["coef_rating"] * -np.log10(results["p_rating"])

    # Normalize scores to 0–1
    results["score_price_norm"] = (results["score_price"] - results["score_price"].min()) / (results["score_price"].max() - results["score_price"].min())
    results["score_rating_norm"] = (results["score_rating"] - results["score_rating"].min()) / (results["score_rating"].max() - results["score_rating"].min())

    # Compute a combined score as the average of normalized price and rating scores
    results["combined_score"] = (results["score_price_norm"] + results["score_rating_norm"]) / 2

    # Sort by combined_score
    results_sorted = results.sort_values("combined_score", ascending=False)

    print("Top features by combined influence on price and rating:")
    print(results_sorted[["combined_score", "coef_price", "coef_rating"]][:10].round(3))