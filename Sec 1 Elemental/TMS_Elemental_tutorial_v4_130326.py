# Imports (This takes about 1 min). Has a few errors and warnings but it seems we can ignore those.
from mastml.mastml import Mastml
from mastml.datasets import LocalDatasets
from mastml.data_cleaning import DataCleaning
from mastml.preprocessing import SklearnPreprocessor
from mastml.models import SklearnModel
from mastml.data_splitters import SklearnDataSplitter, NoSplit
from mastml.mastml_predictor import make_prediction
from mastml.feature_selectors import EnsembleModelFeatureSelector, NoSelect, SklearnFeatureSelector, MASTMLFeatureSelector
from mastml.feature_selectors import ShapFeatureSelector
from mastml.feature_generators import ElementalFeatureGenerator
from mastml.learning_curve import LearningCurve
from mastml.hyper_opt import GridSearch
from mastml.hyper_opt import GridSearch

# Python utilities packages
#!pip install pandas
import os                        # OS stands for Operating System and provides ways for python to interact with files or directories
from collections import Counter  # Collections is a package for handling data
from pprint import pprint

import pandas as pd              # Pandas is a data analysis library which we'll primarily use to handle our dataset
import numpy as np               # Numpy is a package for scientific computing. We'll use it for some of it's math functions
import pymatgen                  # Pymatgen is a library for materials analysis which we use to interpret our material compositions
from pymatgen import core as pymatgen_core       # Needed to get core to be accessible.  Note sure why. 9/5/23.

import matplotlib                # Matplotlib is the plotting package that we'll use throughout the lab
import matplotlib.pyplot as plt
import seaborn as sns            # Seaborn is a Python data visualization library based on matplotlib

#Set up path to directory with input files and where output will be sent. Checks that the path name is assigned correctly.

d = os.getcwd()
os.path.isdir(d)

#load datafile

from mp_api.client import MPRester
import pandas as pd
import pickle
import string
import matplotlib.pyplot as plt
import numpy as np

alphabet_positions = list(enumerate(string.ascii_uppercase, start=0))
print(alphabet_positions)

def Create_tables(formula):
    # Option 1: Pass your API key directly as an argument.
    with MPRester("Xh0gfyYbbnZf0C43AeQyIg5jwWESQPgq") as mpr:
            docs = mpr.materials.summary.search(
                #material_ids = ["mp-13", "mp-14", "mp-665", "mp-4014", "mp-1018027"],
                #fields = ["formula_pretty", "material_id", "elements", "density_atomic", "is_metal", "composition", ],
                formula = formula
            )

    df = pd.DataFrame([doc.dict() for doc in docs])
    df.head()

    with open("docs_PRUEBA.pkl", "wb") as f:
        pickle.dump(df, f)

    with open("docs_PRUEBA.csv", "wb") as f:
        pickle.dump(df, f)

    print("dumped")

    import os
    import shutil

    # Source file path (where docs_PRUEBA.pkl was just created)
    source_file = "docs_PRUEBA.pkl"
    # Destination directory in Google Drive (from the 'd' variable)
    destination_dir = d

    # Ensure the destination directory exists (though drive.mount usually handles this)
    os.makedirs(destination_dir, exist_ok=True)

    # Construct the full destination path
    destination_file = os.path.join(destination_dir, source_file)

    # Copy the file
    #shutil.copyfile(source_file, destination_file)
    print(f"'{source_file}' successfully copied to '{destination_file}'")

    #Show number of rows
    df.shape[0]
    return 

def Run_model(pkl_path, xlsx_path):
    import joblib
    #df = joblib.load(pkl_path)
    df = pd.read_excel(xlsx_path)
    df.head()

    #The data file contains U-MLIP relaxed structures and average voltages for 2288 materials. Let's plot a histogram of the computed average voltages to see their distribution:

    plot_histogram(df)

    # Create X and y as DataFrames
    X = df[['formula_pretty']].copy()
    X.rename(columns={'formula_pretty': 'composition'}, inplace=True) # Rename column to 'composition' for the feature generator
    y = df[['total_magnetization_normalized_vol']].copy()

    # Display combined view
    #display(pd.concat([X, y], axis=1))

    # Generate features
    # Now we generate features with MAST-ML

    # X: DataFrame with a 'composition' column of formula strings
    # e.g., X = pd.DataFrame({'composition': ['Fe2O3', 'Al2O3', 'NiTi']})

    # Build generator from the compositions in X

    # The ElementalFeatureGenerator expects a DataFrame with string formulas in a specified column.
    # X (from previous cell) now correctly contains the 'composition' column with string formulas.

    efg = ElementalFeatureGenerator(
        X,  # Pass X as the required 'featurize_df' positional argument
        feature_types=['composition_avg', 'max' , 'min', 'difference'],    # use available elemental features
        remove_constant_columns=True
    )

    # Generate elemental features. Pass the original X DataFrame, which now has the 'composition' column.
    X_elem, ytemp = efg.evaluate(X=X, y=None, savepath=d, make_new_dir=True)                # returns a DataFrame of features

    # display(X_elem)

    # Fit model
    # This section fits the elemental features with Regression using either a Ridge (a kind of regularized linear model) or Random Forest (a powerful tree based model) model. We also have to option to perform feature reduction by taking just a subset of principle components. The code does an 80/20 train/test split and 5-fold Cross-Validation (CV), which are standard ways to test the data.
    # Start by loading some relevant ML tools (scikit-learn, a widely used ML package) and setting up global variables to control the fit (choice of PCA and model type).

    print("Starting workflow with optional PCA feature reduction...\n")

    # Core sklearn imports
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split, KFold, cross_validate
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.linear_model import Ridge  # <-- added for optional linear model

    # ======= PCA options =======
    USE_PCA = False            # <- turn PCA on/off (True or False)
    PCA_VAR_KEEP = 0.95       # keep 95% variance (sklearn PCA allows float in (0,1])
    # ===========================

    # ======= Model option =======
    MODEL_TYPE = "rf"         # one of: "rf", "ridge"
    # ===========================

    #Now we pull out the X and y features and target wiht right format, cleaning out any data that are not numbers.

    # 1) Prepare data (assumes X_elem dataframe, y array-like)
    print("[1/7] Preparing data...")
    X = X_elem.copy()
    y = df['total_magnetization_normalized_vol'].values.ravel()  # ensure 1D target

    # Keep only numeric columns and drop rows with NaNs/Infs
    X = X.select_dtypes(include=np.number)
    mask = np.isfinite(X).all(axis=1) & np.isfinite(y)
    X, y = X.loc[mask], y[mask]

    print(f"   -> Data after cleaning: {X.shape[0]} samples, {X.shape[1]} features")
    print("   -> Example feature cols:", list(X.columns[:5]), "\n")

    # Build the model pipeline (including choosing the model). This pipeline tells the code the steps needed in the fitting (scaling, PCA, model fit) so we can run them easily and apply them to train and test data.

    # 2) Build the modeling pipeline: [Scaler] -> [PCA?] -> [Model]
    model_name = "RF" if MODEL_TYPE == "rf" else "Ridge"
    print("[2/7] Building pipeline (Scaler -> {} -> {})...".format("PCA" if USE_PCA else "No PCA", model_name))
    steps = [("scaler", StandardScaler())]
    if USE_PCA:
        steps.append(("pca", PCA(n_components=PCA_VAR_KEEP, svd_solver="auto", random_state=0)))

    # choose model
    if MODEL_TYPE == "rf":
        model = RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1)
    elif MODEL_TYPE == "ridge":
        model = Ridge(alpha=1.0, random_state=0)
    else:
        raise ValueError("MODEL_TYPE must be 'rf' or 'ridge'")

    steps.append(("model", model))
    pipe = Pipeline(steps)

    # Set up the Test/Train split, run the fit no train, and evaluate on train and test.

    # 3) Train/test split (80/20)
    print("[3/7] Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=0
    )
    print(f"   -> Train: {X_train.shape}, Test: {X_test.shape}\n")

    # 4) Fit on the training set
    print("[4/7] Fitting pipeline on training data...")
    pipe.fit(X_train, y_train)
    print("   -> Fit complete.")
    if USE_PCA:
        # Access the fitted PCA to report components retained
        pca = pipe.named_steps["pca"]
        print(f"   -> PCA retained {pca.n_components_} components "
            f"({pca.explained_variance_ratio_.sum():.3f} variance)\n")
    else:
        print("   -> PCA disabled.\n")

    # 5) Evaluate on train & test
    print("[5/7] Evaluating holdout performance...")
    def metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        r2 = r2_score(y_true, y_pred)
        return mae, rmse, r2

    y_pred_train = pipe.predict(X_train)
    y_pred_test  = pipe.predict(X_test)

    mae_tr, rmse_tr, r2_tr = metrics(y_train, y_pred_train)
    mae_te, rmse_te, r2_te = metrics(y_test,  y_pred_test)

    print("=== Holdout Performance (80/20 split) ===")
    print(f"Train: MAE={mae_tr:.4f}, RMSE={rmse_tr:.4f}, R²={r2_tr:.4f}")
    print(f"Test : MAE={mae_te:.4f}, RMSE={rmse_te:.4f}, R²={r2_te:.4f}\n")

    # Do cross validation to get good statistics on left out "test" data.

    # 6) 5-fold cross-validation (uses the SAME pipeline to avoid leakage)
    print("[6/7] Running 5-fold cross-validation...")
    cv = KFold(n_splits=5, shuffle=True, random_state=0)
    cv_results = cross_validate(
        pipe, X, y,
        cv=cv,
        scoring={
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error",
            "r2": "r2"
        },
        n_jobs=-1,
        return_train_score=False
    )

    cv_mae  = -cv_results["test_mae"]
    cv_rmse = -cv_results["test_rmse"]
    cv_r2   =  cv_results["test_r2"]

    print("=== 5-Fold Cross-Validation (entire dataset) ===")
    print(f"MAE : mean={cv_mae.mean():.4f} ± {cv_mae.std():.4f}")
    print(f"RMSE: mean={cv_rmse.mean():.4f} ± {cv_rmse.std():.4f}")
    print(f"R²  : mean={cv_r2.mean():.4f} ± {cv_r2.std():.4f}\n")

    # Now plot results as parity plots.

    # 7) Parity plots for Train and Test (side-by-side, smaller)
    print("[7/7] Generating parity plots...")

    plot_tag = "PCA-ON" if USE_PCA else "PCA-OFF"

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))  # smaller plots side by side

    for ax, (y_true, y_pred, title) in zip(
        axes,
        [
            (y_train, y_pred_train, f"Train [{plot_tag}]"),
            (y_test,  y_pred_test,  f"Test  [{plot_tag}]"),
        ],
    ):
        ax.scatter(y_true, y_pred, s=15, alpha=0.7, edgecolor="none")
        lo = min(np.min(y_true), np.min(y_pred))
        hi = max(np.max(y_true), np.max(y_pred))
        ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=1, color="black")
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_xlabel("True")
        ax.set_ylabel("Predicted")
        ax.set_title(title, fontsize=10)

    
    plt.savefig('Magnetization_scatter.png', dpi=300, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
    

    print("\n✅ Workflow complete.")
    return

def plot_histogram(df, dataset='MP', ion='Na'):
        """ 
        Test dafsflsfjlsjlksjeflkjslkfjlskefjlksejflksejflkjlksjflksejlkjflkje
        """ 
        bins = np.arange(0, 0.5, 0.001)

        # Matterverse avg voltage has a bunch of negative values- remove them!

        #CHANGED TO DENSITY, >=0 MEANS ONLY CHOOSE POSITIVE
        df = df[df['total_magnetization'] >=0]

        plt.clf()

        plt.hist(bins=bins, x=df['total_magnetization_normalized_vol'], color='red', edgecolor='black', alpha=0.5, label='Total Magnetization')

        plt.xlabel('Total Magnetization', fontsize=14)
        plt.xticks(fontsize=12)
        plt.ylabel('Number of occurrences', fontsize=14)
        plt.yticks(fontsize=12)
        plt.legend(loc='best')
        plt.savefig('Magnetization_histogram.png', dpi=300, bbox_inches='tight')

        vals = df['total_magnetization']
        print('Magnetization stat')
        fmt = lambda x: np.format_float_positional(x, precision=3, unique=False, fractional=False, trim='k')

        print(f"{'Mean:':25s}{fmt(np.mean(vals)):>12s}")
        print(f"{'Standard deviation:':25s}{fmt(np.std(vals)):>12s}")
        print(f"{'Min:':25s}{fmt(min(vals)):>12s}")
        print(f"{'Max:':25s}{fmt(max(vals)):>12s}")

formula = ["BaTiO3","SrTiO3","CaTiO3", "LaMnO3", "BiFeO3", "SmFeO3", "PbTiO3","CaZrO3", "CaSnO3","SrZrO3",   "BaZrO3", "PbZrO3","BaHfO3", "SrHfO3", "CaHfO3"
                , "KNbO3", "NaNbO3", "KTaO3", "NaTaO3", "SrSnO3","BaSnO3", "CdTiO3","ZnTiO3","CaRuO3", "SrRuO3","BaRuO3", "LaCoO3", "LaNiO3", "LaCrO3", "NdFeO3"
                , "GdFeO3", "DyFeO3","LaFeO3", "TbMnO3", "DyMnO3", "EuTiO3", "YFeO3", "HoMnO3", "ErMnO3","ErMnO3", "CsPbBr3", "CsPbCl3", "CsSnI3", "CsSnI3"
                , "CsSnBr3", "FAPbBr3", "FASnI3", "MAPbCl3", "LaAlO3", "NdAlO3", "PrAlO3", "SmAlO3", "GdAlO3", "CaNbO3", "SrNbO3", "BaNbO3", "CaTaO3", "SrTaO3"
                , "BaTaO3", "CaMoO3", "SrMoO3", "BaMoO3", "CaWO3", "SrWO3", "BaWO3", "NdMnO3", "PrMnO3", "SmMnO3", "GdMnO3", "TbFeO3", "ErFeO3", "YbFeO3"
                , "CsGeI3", "CsGeBr3", "CsGeCl3", "MaSnCl3", "FASnBr3", "LaCuO3","CaCuO3", "SrCuO3", "BaPbO3", "SrIrO3", "CaIrO3"]

pkl_path = "/home/diegop/Documents/Pymatgen-2026/perovskites_sample.pkl"
xlsx_path = "/home/diegop/Documents/Pymatgen-2026/perovskites_sample_full.xlsx"

#Create_tables(formula)
Run_model(pkl_path, xlsx_path)

"""
That is a complete fit and assessment with test data and cross-validation. To explore further, consider trying the following
1. Change MODEL_TYPE to "rf" for Random Forest. This is a more sophisticated ML method than ridge and gives significantly better results. However, it is slower (takes ~1min on my google colab CPU).
2. Try turning off PCA. This will then use the full feature set, which gives the best possible features but can take a long time with random forest (about 3m on my google colab CPU).  


Here were my final best statistics (but maybe you can beat them!)

[5/7] Evaluating holdout performance...

=== Holdout Performance (80/20 split) ===

Train: MAE=0.1045, RMSE=0.1721, R²=0.9645

Test : MAE=0.2601, RMSE=0.4285, R²=0.7872

[6/7] Running 5-fold cross-validation...

=== 5-Fold Cross-Validation (entire dataset) ===

MAE : mean=0.2479 ± 0.0089

RMSE: mean=0.4153 ± 0.0132

R²  : mean=0.7929 ± 0.0173
"""

# Backup
# The Following is backup in useful single cell format.

'''
# Code in one cell for easy updating.
# --- Random Forest regression with optional PCA reduction, 80/20 split + 5-fold CV ---

print("Starting RF workflow with optional PCA feature reduction...\n")

# Core sklearn imports
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge  # <-- added for optional linear model

# ======= PCA options =======
USE_PCA = True            # <- turn PCA on/off
PCA_VAR_KEEP = 0.95       # keep 95% variance (sklearn PCA allows float in (0,1])
# ===========================

# ======= Model option =======
MODEL_TYPE = "ridge"         # one of: "rf", "ridge"
# ===========================

# 1) Prepare data (assumes X_elem dataframe, y array-like)
print("[1/7] Preparing data...")
X = X_elem.copy()
y = df['Average voltage (V/ion)'].values.ravel()  # ensure 1D target

# Keep only numeric columns and drop rows with NaNs/Infs
X = X.select_dtypes(include=np.number)
mask = np.isfinite(X).all(axis=1) & np.isfinite(y)
X, y = X.loc[mask], y[mask]

print(f"   -> Data after cleaning: {X.shape[0]} samples, {X.shape[1]} features")
print("   -> Example feature cols:", list(X.columns[:5]), "\n")

# 2) Build the modeling pipeline: [Scaler] -> [PCA?] -> [Model]
model_name = "RF" if MODEL_TYPE == "rf" else "Ridge"
print("[2/7] Building pipeline (Scaler -> {} -> {})...".format("PCA" if USE_PCA else "No PCA", model_name))
steps = [("scaler", StandardScaler())]
if USE_PCA:
    steps.append(("pca", PCA(n_components=PCA_VAR_KEEP, svd_solver="auto", random_state=0)))

# choose model
if MODEL_TYPE == "rf":
    model = RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1)
elif MODEL_TYPE == "ridge":
    model = Ridge(alpha=1.0, random_state=0)
else:
    raise ValueError("MODEL_TYPE must be 'rf' or 'ridge'")

steps.append(("model", model))
pipe = Pipeline(steps)

# 3) Train/test split (80/20)
print("[3/7] Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0
)
print(f"   -> Train: {X_train.shape}, Test: {X_test.shape}\n")

# 4) Fit on the training set
print("[4/7] Fitting pipeline on training data...")
pipe.fit(X_train, y_train)
print("   -> Fit complete.")
if USE_PCA:
    # Access the fitted PCA to report components retained
    pca = pipe.named_steps["pca"]
    print(f"   -> PCA retained {pca.n_components_} components "
          f"({pca.explained_variance_ratio_.sum():.3f} variance)\n")
else:
    print("   -> PCA disabled.\n")

# 5) Evaluate on train & test
print("[5/7] Evaluating holdout performance...")
def metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2

y_pred_train = pipe.predict(X_train)
y_pred_test  = pipe.predict(X_test)

mae_tr, rmse_tr, r2_tr = metrics(y_train, y_pred_train)
mae_te, rmse_te, r2_te = metrics(y_test,  y_pred_test)

print("=== Holdout Performance (80/20 split) ===")
print(f"Train: MAE={mae_tr:.4f}, RMSE={rmse_tr:.4f}, R²={r2_tr:.4f}")
print(f"Test : MAE={mae_te:.4f}, RMSE={rmse_te:.4f}, R²={r2_te:.4f}\n")

# 6) 5-fold cross-validation (uses the SAME pipeline to avoid leakage)
print("[6/7] Running 5-fold cross-validation...")
cv = KFold(n_splits=5, shuffle=True, random_state=0)
cv_results = cross_validate(
    pipe, X, y,
    cv=cv,
    scoring={
        "mae": "neg_mean_absolute_error",
        "rmse": "neg_root_mean_squared_error",
        "r2": "r2"
    },
    n_jobs=-1,
    return_train_score=False
)

cv_mae  = -cv_results["test_mae"]
cv_rmse = -cv_results["test_rmse"]
cv_r2   =  cv_results["test_r2"]

print("=== 5-Fold Cross-Validation (entire dataset) ===")
print(f"MAE : mean={cv_mae.mean():.4f} ± {cv_mae.std():.4f}")
print(f"RMSE: mean={cv_rmse.mean():.4f} ± {cv_rmse.std():.4f}")
print(f"R²  : mean={cv_r2.mean():.4f} ± {cv_r2.std():.4f}\n")

# 7) Parity plots for Train and Test (side-by-side, smaller)
print("[7/7] Generating parity plots...")

import matplotlib.pyplot as plt
import numpy as np

plot_tag = "PCA-ON" if USE_PCA else "PCA-OFF"

fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))  # smaller plots side by side

for ax, (y_true, y_pred, title) in zip(
    axes,
    [
        (y_train, y_pred_train, f"Train [{plot_tag}]"),
        (y_test,  y_pred_test,  f"Test  [{plot_tag}]"),
    ],
):
    ax.scatter(y_true, y_pred, s=15, alpha=0.7, edgecolor="none")
    lo = min(np.min(y_true), np.min(y_pred))
    hi = max(np.max(y_true), np.max(y_pred))
    ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=1, color="black")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("True")
    ax.set_ylabel("Predicted")
    ax.set_title(title, fontsize=10)

plt.tight_layout()
plt.show()

print("\n✅ Workflow complete.")
'''