# #%% Imports
# import numpy as np
# import pandas as pd
# from scipy.stats import ttest_ind
# from scipy.stats import levene
# import matplotlib.pyplot as plt
# from sklearn.svm import SVC
# from sklearn.model_selection import KFold
# from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score
# from sklearn.preprocessing import RobustScaler
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import KFold
# from sklearn.svm import SVC
# from sklearn.metrics import (
#     accuracy_score, 
#     recall_score, 
#     confusion_matrix, 
#     f1_score
# )
# from sklearn.preprocessing import StandardScaler
# import numpy as np
# import pandas as pd




# #%% Import features from the excel file

# path = 'Features-2.xlsx'
# AD = pd.read_excel(path, sheet_name='AD')
# AD_SUVR_ref = pd.read_excel(path, sheet_name='AD-ref')

# MCI = pd.read_excel(path, sheet_name='MCI')
# MCI_SUVR_ref = pd.read_excel(path, sheet_name='MCI-ref')

# NC = pd.read_excel(path, sheet_name='NC')
# NC_SUVR_ref = pd.read_excel(path, sheet_name='NC-ref')


# # Calculate SUVR
# for i in range (120):
#     AD.iloc[i, 2:117] /= AD_SUVR_ref.iloc[i,0]
#     MCI.iloc[i, 2:117] /= MCI_SUVR_ref.iloc[i,0]
#     NC.iloc[i, 2:117] /= NC_SUVR_ref.iloc[i,0]


# '''
# col 0 -> Subjects
# col 1 -> Group
# col 2:20 -> subcortical SUVR
# col 21:116 -> cortical SUVR
# col 117:135 -> subcortical volume
# col 136:231 -> cortical volume
# col 232 -> MHPSYCH
# col 233 -> MH2NEURL
# col 234 -> MH4CARD
# col 235 -> MMSCORE
# col 236 -> CLINICAL DEMENTIA RATING
# '''


# # Mean & SD
# AD_mean = AD.mean(numeric_only=True)
# MCI_mean = MCI.mean(numeric_only=True)
# NC_mean = NC.mean(numeric_only=True)

# AD_SD = AD.std(numeric_only=True)
# MCI_SD = MCI.std(numeric_only=True)
# NC_SD = NC.std(numeric_only=True)





# #%% Outlier handling

# def replace_outliers_with_median(df, columns):
#     for col in columns:
#         Q1 = np.percentile(df[col], 25)
#         Q3 = np.percentile(df[col], 75)
#         IQR = Q3 - Q1
#         lower_bound = Q1 - 1.5 * IQR
#         upper_bound = Q3 + 1.5 * IQR
        
#         # Replace outliers with the mean or median (change below if you want median)
#         df[col] = df[col].apply(lambda x: np.median(df[col]) if x < lower_bound or x > upper_bound else x)
#     return df




# collumns_to_check = AD.columns[2:232]
# AD = replace_outliers_with_median(AD, collumns_to_check)
# MCI = replace_outliers_with_median(MCI, collumns_to_check)
# NC = replace_outliers_with_median(NC, collumns_to_check)





# #%% initiations

# results_suvr_all = pd.DataFrame(AD.columns[2:117], columns=['ROI'])
# results_suvr_AD_vs_MCI = []
# results_suvr_MCI_vs_NC = []
# results_suvr_AD_vs_NC = []

# results_volume_all = pd.DataFrame(AD.columns[117:232], columns=['ROI'])
# results_volume_AD_vs_MCI = []
# results_volume_MCI_vs_NC = []
# results_volume_AD_vs_NC = []







# # %% AD vs. MCI (SUVR)
# num_of_ROIs = 0
# for i in range(2, 117):
#     group1 = AD.iloc[:,i]
#     group2 = MCI.iloc[:,i]
#     corrected_type_I_error = 0.05/115
    
#     # equality of variance
#     stat, p_value = levene(group1, group2)
#     if p_value < corrected_type_I_error:
#         var_equal = False
#     else:
#         var_equal = True

#     # two sample t-test
#     t_stat, p_value = ttest_ind(group1, group2, equal_var = var_equal)
#     if p_value < corrected_type_I_error:
#         print(AD.columns[i])
#         results_suvr_AD_vs_MCI.append(1)
#         num_of_ROIs += 1
#     else:
#         results_suvr_AD_vs_MCI.append(0)

# print(f"Number of ROIs: {num_of_ROIs}")
# results_suvr_AD_vs_MCI = pd.DataFrame(results_suvr_AD_vs_MCI, columns=['suvr_AD_vs_MCI'])
# results_suvr_all['suvr_AD_vs_MCI'] = results_suvr_AD_vs_MCI


# # %% MCI vs. NC (SUVR)
# num_of_ROIs = 0
# for i in range(2, 117):
#     group1 = MCI.iloc[:,i]
#     group2 = NC.iloc[:,i]
#     corrected_type_I_error = 0.05/115
    
#     # equality of variance
#     stat, p_value = levene(group1, group2)
#     if p_value < corrected_type_I_error:
#         var_equal = False
#     else:
#         var_equal = True

#     # two sample t-test
#     t_stat, p_value = ttest_ind(group1, group2, equal_var = var_equal)
#     if p_value < corrected_type_I_error:
#         print(AD.columns[i])
#         results_suvr_MCI_vs_NC.append(1)
#         num_of_ROIs += 1
#     else:
#         results_suvr_MCI_vs_NC.append(0)

# print(f"Number of ROIs: {num_of_ROIs}")
# results_suvr_MCI_vs_NC = pd.DataFrame(results_suvr_MCI_vs_NC, columns=['suvr_MCI_vs_NC'])
# results_suvr_all['suvr_MCI_vs_NC'] = results_suvr_MCI_vs_NC


# # %% AD vs. NC (SUVR)
# num_of_ROIs = 0
# for i in range(2, 117):
#     group1 = AD.iloc[:,i]
#     group2 = NC.iloc[:,i]
#     corrected_type_I_error = 0.05/115
    
#     # equality of variance
#     stat, p_value = levene(group1, group2)
#     if p_value < corrected_type_I_error:
#         var_equal = False
#     else:
#         var_equal = True

#     # two sample t-test
#     t_stat, p_value = ttest_ind(group1, group2, equal_var = var_equal)
#     if p_value < corrected_type_I_error:
#         print(AD.columns[i])
#         results_suvr_AD_vs_NC.append(1)
#         num_of_ROIs += 1
#     else:
#         results_suvr_AD_vs_NC.append(0)

# print(f"Number of ROIs: {num_of_ROIs}")
# results_suvr_AD_vs_MCI = pd.DataFrame(results_suvr_AD_vs_NC, columns=['suvr_AD_vs_NC'])
# results_suvr_all['suvr_AD_vs_NC'] = results_suvr_AD_vs_NC





# # %% AD vs. MCI (volume)
# num_of_ROIs = 0
# for i in range(117, 232):
#     group1 = AD.iloc[:,i]
#     group2 = MCI.iloc[:,i]
#     corrected_type_I_error = 0.05/115
    
#     # equality of variance
#     stat, p_value = levene(group1, group2)
#     if p_value < corrected_type_I_error:
#         var_equal = False
#     else:
#         var_equal = True

#     # two sample t-test
#     t_stat, p_value = ttest_ind(group1, group2, equal_var = var_equal)
#     if p_value < corrected_type_I_error:
#         print(AD.columns[i])
#         results_volume_AD_vs_MCI.append(1)
#         num_of_ROIs += 1
#     else:
#         results_volume_AD_vs_MCI.append(0)

# print(f"Number of ROIs: {num_of_ROIs}")
# results_volume_AD_vs_MCI = pd.DataFrame(results_volume_AD_vs_MCI, columns=['volume_AD_vs_MCI'])
# results_volume_all['volume_AD_vs_MCI'] = results_volume_AD_vs_MCI



# # %% MCI vs. NC (volume)
# num_of_ROIs = 0
# for i in range(117, 232):
#     group1 = MCI.iloc[:,i]
#     group2 = NC.iloc[:,i]
#     corrected_type_I_error = 0.05/115
    
#     # equality of variance
#     stat, p_value = levene(group1, group2)
#     if p_value < corrected_type_I_error:
#         var_equal = False
#     else:
#         var_equal = True

#     # two sample t-test
#     t_stat, p_value = ttest_ind(group1, group2, equal_var = var_equal)
#     if p_value < corrected_type_I_error:
#         print(AD.columns[i])
#         results_volume_MCI_vs_NC.append(1)
#         num_of_ROIs += 1
#     else:
#         results_volume_MCI_vs_NC.append(0)

# print(f"Number of ROIs: {num_of_ROIs}")
# results_volume_MCI_vs_NC = pd.DataFrame(results_volume_MCI_vs_NC, columns=['volume_MCI_vs_NC'])
# results_volume_all['volume_MCI_vs_NC'] = results_volume_MCI_vs_NC


# # %% AD vs. NC (volume)
# num_of_ROIs = 0
# for i in range(117, 232):
#     group1 = AD.iloc[:,i]
#     group2 = NC.iloc[:,i]
#     corrected_type_I_error = 0.05/115
    
#     # equality of variance
#     stat, p_value = levene(group1, group2)
#     if p_value < corrected_type_I_error:
#         var_equal = False
#     else:
#         var_equal = True

#     # two sample t-test
#     t_stat, p_value = ttest_ind(group1, group2, equal_var = var_equal)
#     if p_value < corrected_type_I_error:
#         print(AD.columns[i])
#         results_volume_AD_vs_NC.append(1)
#         num_of_ROIs += 1
#     else:
#         results_volume_AD_vs_NC.append(0)

# print(f"Number of ROIs: {num_of_ROIs}")
# results_volume_MCI_vs_NC = pd.DataFrame(results_volume_AD_vs_NC, columns=['volume_AD_vs_NC'])
# results_volume_all['volume_AD_vs_NC'] = results_volume_AD_vs_NC




# # %% Plot

# AD.describe()
# MCI.describe()
# NC.describe()


# temp1 = pd.DataFrame(AD.mean(numeric_only=True))
# temp2 = pd.DataFrame(MCI.mean(numeric_only=True))
# temp3 = pd.DataFrame(NC.mean(numeric_only=True))

# #drop left and right whole crebral cortex for the sake of plotting
# temp1 = temp1.drop('1_left_cerebral_cortex_SUVR,')
# temp1 = temp1.drop('11_right_cerebral_cortex_SUVR,')
# temp1 = temp1.drop('11_right_cerebral_cortex_volume,')
# temp1 = temp1.drop('1_left_cerebral_cortex_volume,')
# temp2 = temp2.drop('1_left_cerebral_cortex_SUVR,')
# temp2 = temp2.drop('11_right_cerebral_cortex_SUVR,')
# temp2 = temp2.drop('11_right_cerebral_cortex_volume,')
# temp2 = temp2.drop('1_left_cerebral_cortex_volume,')
# temp3 = temp3.drop('1_left_cerebral_cortex_SUVR,')
# temp3 = temp3.drop('11_right_cerebral_cortex_SUVR,')
# temp3 = temp3.drop('11_right_cerebral_cortex_volume,')
# temp3 = temp3.drop('1_left_cerebral_cortex_volume,')


# # Define larger font sizes
# plt.rcParams.update({
#     'font.size': 14,        # General font size
#     'axes.titlesize': 16,   # Title font size
#     'axes.labelsize': 14,   # Axes labels font size
#     'xtick.labelsize': 12,  # X-axis tick labels font size
#     'ytick.labelsize': 12,  # Y-axis tick labels font size
#     'legend.fontsize': 12   # Legend font size
# })

# # Create subplots for better layout
# fig, axes = plt.subplots(2, 1, figsize=(12, 10), constrained_layout=True)

# # Plot SUVR Mean Comparison (No lines, only markers)
# axes[0].plot(
#     temp1.iloc[0:113], label='AD', color='red', marker='o', linestyle='None', markersize=6, alpha=0.8
# )
# axes[0].plot(
#     temp2.iloc[0:113], label='MCI', color='orange', marker='s', linestyle='None', markersize=6, alpha=0.8
# )
# axes[0].plot(
#     temp3.iloc[0:113], label='NC', color='green', marker='^', linestyle='None', markersize=6, alpha=0.8
# )
# axes[0].set_xlabel('ROI')
# axes[0].set_ylabel('Average SUVR')
# #axes[0].set_title('Average SUVR Comparison')
# axes[0].grid(True, linestyle='--', alpha=0.5)
# axes[0].legend()

# # Plot Volume Mean Comparison (No lines, only markers)
# axes[1].plot(
#     temp1.iloc[115:228], label='AD', color='red', marker='o', linestyle='None', markersize=6, alpha=0.8
# )
# axes[1].plot(
#     temp2.iloc[115:228], label='MCI', color='orange', marker='s', linestyle='None', markersize=6, alpha=0.8
# )
# axes[1].plot(
#     temp3.iloc[115:228], label='NC', color='green', marker='^', linestyle='None', markersize=6, alpha=0.8
# )
# axes[1].set_xlabel('ROI')
# axes[1].set_ylabel('Average Volume (mm$^3$)')
# #axes[1].set_title('Average Volume Comparison')
# axes[1].grid(True, linestyle='--', alpha=0.5)
# axes[1].legend()

# # Show the final plots
# plt.show()


# #%%

# # Prepare data for boxplot (SUVR)
# data1 = temp1.iloc[0:113].values.flatten()  # Flatten to 1D array if it's 2D
# data2 = temp2.iloc[0:113].values.flatten()
# data3 = temp3.iloc[0:113].values.flatten()

# # Combine the data for boxplot (SUVR)
# temp_SUVR = [data1, data2, data3]

# # Create the boxplot for SUVR
# plt.figure(figsize=(8, 6))
# plt.boxplot(temp_SUVR, labels=['AD', 'MCI', 'NC'])
# plt.title("Boxplot of SUVR by Group")
# plt.xlabel("Groups")
# plt.ylabel("SUVR")
# plt.grid(True, linestyle='--', alpha=0.5)  # Add grid for better readability
# plt.show()

# # Prepare data for boxplot (Volume)
# data1 = temp1.iloc[115:228].values.flatten()  # Flatten to 1D array if it's 2D
# data2 = temp2.iloc[115:228].values.flatten()
# data3 = temp3.iloc[115:228].values.flatten()

# # Combine the data for boxplot (Volume)
# temp_SUVR = [data1, data2, data3]

# # Create the boxplot for Volume
# plt.figure(figsize=(8, 6))
# plt.boxplot(temp_SUVR, labels=['AD', 'MCI', 'NC'])
# plt.title("Boxplot of Volume by Group")
# plt.xlabel("Groups")
# plt.ylabel("Volume (mm³)")
# plt.grid(True, linestyle='--', alpha=0.5)  # Add grid for better readability
# plt.show()








# #%% SVM AD vs. MCI

# group1 = AD
# group2 = MCI

# #Comment out the following lines if you want to include all ROIs
# for i in range(len(results_suvr_all)):
#     if results_suvr_all.iloc[i, 1] == 0:
#         group1 = group1.drop([results_suvr_all.iloc[i, 0]], axis=1)
#         group2 = group2.drop([results_suvr_all.iloc[i, 0]], axis=1)

# for i in range(len(results_volume_all)):
#     if results_volume_all.iloc[i, 1] == 0:
#         group1 = group1.drop([results_volume_all.iloc[i, 0]], axis=1)
#         group2 = group2.drop([results_volume_all.iloc[i, 0]], axis=1)
# #until here

# data = pd.concat([group1, group2], axis=0).reset_index(drop=True)

# # Scaling the data
# scaler1 = RobustScaler();
# scaler2 = StandardScaler();
# data.iloc[:, 2:] = scaler1.fit_transform(data.iloc[:, 2:]);





# #%%
# # Separate features and labels
# X = data.iloc[:, 2:].values  # Features
# y = data.iloc[:, 1].values   # Labels

# # Feature scaling (standardize features to zero mean and unit variance)
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

# # Initialize 5-fold cross-validation
# # All features: random_state=20
# # Selected features: random_state=20
# kf = KFold(n_splits=10, shuffle=True, random_state=20)

# # Define a parameter grid for C (regularization strength)
# param_grid = {
#     'C': [0.1, 1, 10, 100],  # Try different values for C
#     'kernel': ['linear'],  # Only using linear kernel
#     'class_weight': ['balanced']  # Account for class imbalance
# }

# # Initialize GridSearchCV with the SVM model
# grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=kf, scoring='accuracy')

# # Initialize performance metrics
# accuracy_scores = []
# sensitivity_scores = []
# specificity_scores = []
# f1_scores = []

# for fold, (train_index, test_index) in enumerate(kf.split(X), 1):
#     # Split data into training and testing sets for this fold
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]
    
#     # Perform grid search to find the best SVM model
#     grid_search.fit(X_train, y_train)
    
#     # Get the best model from grid search
#     best_svm = grid_search.best_estimator_
    
#     # Predict on test data
#     y_pred = best_svm.predict(X_test)
    
#     # Calculate metrics
#     acc = accuracy_score(y_test, y_pred)
#     f1 = f1_score(y_test, y_pred, average='weighted')  # Weighted for imbalanced classes
    
#     # Sensitivity (Recall for the positive class, e.g., 'AD')
#     sensitivity = recall_score(y_test, y_pred, pos_label='AD', zero_division=0)
    
#     # Specificity (Recall for the negative class, e.g., 'MCI')
#     cm = confusion_matrix(y_test, y_pred, labels=['AD', 'MCI'])
#     if cm.shape == (2, 2):
#         tn, fp, fn, tp = cm.ravel()
#         specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
#     else:
#         specificity = 0  # Handle cases where confusion matrix shape is invalid
    
#     # Print metrics for this fold
#     print(f"Fold {fold} Metrics:")
#     print(f"Accuracy: {acc:.2f}")
#     print(f"Sensitivity: {sensitivity:.2f}")
#     print(f"Specificity: {specificity:.2f}")
#     print(f"F1 Score: {f1:.2f}")
#     print(f"Best C: {grid_search.best_params_['C']}")
#     print('-' * 40)
    
#     # Append metrics for averaging later
#     accuracy_scores.append(acc)
#     sensitivity_scores.append(sensitivity)
#     specificity_scores.append(specificity)
#     f1_scores.append(f1)

# # Calculate average metrics across all folds
# mean_accuracy = np.mean(accuracy_scores)
# mean_sensitivity = np.mean(sensitivity_scores)
# mean_specificity = np.mean(specificity_scores)
# mean_f1 = np.mean(f1_scores)

# # Print overall results
# print("Average Metrics:")
# print(f"Accuracy: {mean_accuracy:.2f}")
# print(f"Sensitivity: {mean_sensitivity:.2f}")
# print(f"Specificity: {mean_specificity:.2f}")
# print(f"F1 Score: {mean_f1:.2f}")












# #%% SVM MCI vs. NC

# group1 = MCI
# group2 = NC

# # Comment out the following lines if you want to include all ROIs
# for i in range(len(results_suvr_all)):
#     if results_suvr_all.iloc[i, 2] == 0:
#         group1 = group1.drop([results_suvr_all.iloc[i, 0]], axis=1)
#         group2 = group2.drop([results_suvr_all.iloc[i, 0]], axis=1)

# for i in range(len(results_volume_all)):
#     if results_volume_all.iloc[i, 2] == 0:
#         group1 = group1.drop([results_volume_all.iloc[i, 0]], axis=1)
#         group2 = group2.drop([results_volume_all.iloc[i, 0]], axis=1)
# # until here

# # Combine the data from MCI and NC groups
# data = pd.concat([group1, group2], axis=0).reset_index(drop=True)

# # Scaling the data (you can keep using either scaler based on your preference)
# scaler1 = RobustScaler()  # Keep this or use StandardScaler if preferred
# data.iloc[:, 2:] = scaler1.fit_transform(data.iloc[:, 2:])





# #%%
# # Separate features and labels
# X = data.iloc[:, 2:].values  # Features
# y = data.iloc[:, 1].values   # Labels

# # Feature scaling (standardize features to zero mean and unit variance)
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

# # Initialize 5-fold cross-validation
# # All features: random_state=41
# # Selected features: random_state=20
# kf = KFold(n_splits=10, shuffle=True, random_state=20)

# # Define a parameter grid for C (regularization strength)
# param_grid = {
#     'C': [0.1, 1, 10, 100],  # Try different values for C
#     'kernel': ['linear'],  # Only using linear kernel
#     'class_weight': ['balanced']  # Account for class imbalance
# }

# # Initialize GridSearchCV with the SVM model
# grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=kf, scoring='accuracy')

# # Initialize performance metrics
# accuracy_scores = []
# sensitivity_scores = []
# specificity_scores = []
# f1_scores = []

# for fold, (train_index, test_index) in enumerate(kf.split(X), 1):
#     # Split data into training and testing sets for this fold
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]
    
#     # Perform grid search to find the best SVM model
#     grid_search.fit(X_train, y_train)
    
#     # Get the best model from grid search
#     best_svm = grid_search.best_estimator_
    
#     # Predict on test data
#     y_pred = best_svm.predict(X_test)
    
#     # Calculate metrics
#     acc = accuracy_score(y_test, y_pred)
#     f1 = f1_score(y_test, y_pred, average='weighted')  # Weighted for imbalanced classes
    
#     # Sensitivity (Recall for the positive class, e.g., 'MCI')
#     sensitivity = recall_score(y_test, y_pred, pos_label='MCI', zero_division=0)
    
#     # Specificity (Recall for the negative class, e.g., 'MCI')
#     cm = confusion_matrix(y_test, y_pred, labels=['MCI', 'NC'])
#     if cm.shape == (2, 2):
#         tn, fp, fn, tp = cm.ravel()
#         specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
#     else:
#         specificity = 0  # Handle cases where confusion matrix shape is invalid
    
#     # Print metrics for this fold
#     print(f"Fold {fold} Metrics:")
#     print(f"Accuracy: {acc:.2f}")
#     print(f"Sensitivity: {sensitivity:.2f}")
#     print(f"Specificity: {specificity:.2f}")
#     print(f"F1 Score: {f1:.2f}")
#     print(f"Best C: {grid_search.best_params_['C']}")
#     print('-' * 40)
    
#     # Append metrics for averaging later
#     accuracy_scores.append(acc)
#     sensitivity_scores.append(sensitivity)
#     specificity_scores.append(specificity)
#     f1_scores.append(f1)

# # Calculate average metrics across all folds
# mean_accuracy = np.mean(accuracy_scores)
# mean_sensitivity = np.mean(sensitivity_scores)
# mean_specificity = np.mean(specificity_scores)
# mean_f1 = np.mean(f1_scores)

# # Print overall results
# print("Average Metrics:")
# print(f"Accuracy: {mean_accuracy:.2f}")
# print(f"Sensitivity: {mean_sensitivity:.2f}")
# print(f"Specificity: {mean_specificity:.2f}")
# print(f"F1 Score: {mean_f1:.2f}")









# #%% SVM AD vs. NC

# group1 = AD
# group2 = NC

# # Comment out the following lines if you want to include all ROIs
# for i in range(len(results_suvr_all)):
#     if results_suvr_all.iloc[i, 3] == 0:
#         group1 = group1.drop([results_suvr_all.iloc[i, 0]], axis=1)
#         group2 = group2.drop([results_suvr_all.iloc[i, 0]], axis=1)

# for i in range(len(results_volume_all)):
#     if results_volume_all.iloc[i, 3] == 0:
#         group1 = group1.drop([results_volume_all.iloc[i, 0]], axis=1)
#         group2 = group2.drop([results_volume_all.iloc[i, 0]], axis=1)
# # until here

# # Combine the data from MCI and NC groups
# data = pd.concat([group1, group2], axis=0).reset_index(drop=True)

# # Scaling the data (you can keep using either scaler based on your preference)
# scaler1 = RobustScaler()  # Keep this or use StandardScaler if preferred
# data.iloc[:, 2:] = scaler1.fit_transform(data.iloc[:, 2:])





# #%%
# # Separate features and labels
# X = data.iloc[:, 2:].values  # Features
# y = data.iloc[:, 1].values   # Labels

# # Feature scaling (standardize features to zero mean and unit variance)
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

# # Initialize 5-fold cross-validation
# # All features: random_state=41
# # Selected features: random_state=20
# kf = KFold(n_splits=10, shuffle=True, random_state=20)

# # Define a parameter grid for C (regularization strength)
# param_grid = {
#     'C': [0.1, 1, 10, 100],  # Try different values for C
#     'kernel': ['linear'],  # Only using linear kernel
#     'class_weight': ['balanced']  # Account for class imbalance
# }

# # Initialize GridSearchCV with the SVM model
# grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=kf, scoring='accuracy')

# # Initialize performance metrics
# accuracy_scores = []
# sensitivity_scores = []
# specificity_scores = []
# f1_scores = []

# for fold, (train_index, test_index) in enumerate(kf.split(X), 1):
#     # Split data into training and testing sets for this fold
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]
    
#     # Perform grid search to find the best SVM model
#     grid_search.fit(X_train, y_train)
    
#     # Get the best model from grid search
#     best_svm = grid_search.best_estimator_
    
#     # Predict on test data
#     y_pred = best_svm.predict(X_test)
    
#     # Calculate metrics
#     acc = accuracy_score(y_test, y_pred)
#     f1 = f1_score(y_test, y_pred, average='weighted')  # Weighted for imbalanced classes
    
#     # Sensitivity (Recall for the positive class, e.g., 'AD')
#     sensitivity = recall_score(y_test, y_pred, pos_label='AD', zero_division=0)
    
#     # Specificity (Recall for the negative class, e.g., 'AD')
#     cm = confusion_matrix(y_test, y_pred, labels=['AD', 'NC'])
#     if cm.shape == (2, 2):
#         tn, fp, fn, tp = cm.ravel()
#         specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
#     else:
#         specificity = 0  # Handle cases where confusion matrix shape is invalid
    
#     # Print metrics for this fold
#     print(f"Fold {fold} Metrics:")
#     print(f"Accuracy: {acc:.2f}")
#     print(f"Sensitivity: {sensitivity:.2f}")
#     print(f"Specificity: {specificity:.2f}")
#     print(f"F1 Score: {f1:.2f}")
#     print(f"Best C: {grid_search.best_params_['C']}")
#     print('-' * 40)
    
#     # Append metrics for averaging later
#     accuracy_scores.append(acc)
#     sensitivity_scores.append(sensitivity)
#     specificity_scores.append(specificity)
#     f1_scores.append(f1)

# # Calculate average metrics across all folds
# mean_accuracy = np.mean(accuracy_scores)
# mean_sensitivity = np.mean(sensitivity_scores)
# mean_specificity = np.mean(specificity_scores)
# mean_f1 = np.mean(f1_scores)

# # Print overall results
# print("Average Metrics:")
# print(f"Accuracy: {mean_accuracy:.2f}")
# print(f"Sensitivity: {mean_sensitivity:.2f}")
# print(f"Specificity: {mean_specificity:.2f}")
# print(f"F1 Score: {mean_f1:.2f}")





#%% plot 2

import numpy as np
import matplotlib.pyplot as plt

# Data for the visualization
comparisons = ['AD vs. MCI', 'MCI vs. NC', 'AD vs. NC']
metrics = ['Accuracy', 'Sensitivity', 'Specificity', 'F1 Score']

# Results for all features and selected features
all_features = {
    'Accuracy': [76, 83, 88],
    'Sensitivity': [77, 85, 88],
    'Specificity': [77, 85, 88],
    'F1 Score': [76, 83, 87]
}

selected_features = {
    'Accuracy': [70, 79, 86],
    'Sensitivity': [68, 78, 87],
    'Specificity': [68, 78, 87],
    'F1 Score': [70, 79, 86]
}

# Bar width and x positions
bar_width = 0.35
x = np.arange(len(comparisons))

# Create the subplots
fig, axs = plt.subplots(2, 2, figsize=(11, 11))
# fig.suptitle('SVM Classification Metrics (Averaged Over 10 Folds)', fontsize=16)

for i, metric in enumerate(metrics):
    ax = axs[i // 2, i % 2]  # Position the subplot
    bars_all = ax.bar(x - bar_width / 2, all_features[metric], bar_width, label='All Features', color='steelblue')
    bars_selected = ax.bar(x + bar_width / 2, selected_features[metric], bar_width, label='Selected Features', color='red')

    # Adding details
    # ax.set_title(metric, fontsize=16)
    # ax.set_xlabel('Comparison', fontsize=16)
    ax.set_ylabel(f'{metric} (%)', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(comparisons, fontsize=16)
    ax.set_ylim(0, 100)
    ax.legend()

    # Annotating bars with values
    for bar in bars_all + bars_selected:
        height = bar.get_height()
        ax.annotate(f'{height}%', 
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Offset for text
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=16)

# Adjust layout and show the plot
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Add space for the title
plt.show()



# %%
