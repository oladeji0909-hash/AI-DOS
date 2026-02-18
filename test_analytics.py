import requests
import json

BASE_URL = "http://localhost:8008"

print("=== ANALYTICS SERVICE TEST ===\n")

# 1. Dashboard Summary
print("1. Dashboard Summary...")
response = requests.get(f"{BASE_URL}/analytics/dashboard/summary")
summary = response.json()
print(f"Total Models: {summary['total_models']}")
print(f"Total Experiments: {summary['total_experiments']}")
print(f"Total Deployments: {summary['total_deployments']}")
print(f"Predictions Today: {summary['total_predictions_today']}")
print(f"Avg Model Accuracy: {summary['avg_model_accuracy']}")
print(f"Total Revenue: ${summary['total_revenue']}")

# 2. Model Performance
print("\n2. Model Performance Analytics...")
response = requests.get(f"{BASE_URL}/analytics/model/model_123/performance?time_range=week")
perf = response.json()
print(f"Model: {perf['model_id']}")
print(f"Total Predictions: {perf['total_predictions']}")
print(f"Avg Response Time: {perf['avg_response_time']}ms")
print(f"Error Rate: {perf['error_rate']*100}%")
print(f"Accuracy Trend (last 3 days):")
for day in perf['accuracy_trend'][-3:]:
    print(f"  {day['date']}: {day['accuracy']}")

# 3. Confusion Matrix
print("\n3. Confusion Matrix...")
response = requests.get(f"{BASE_URL}/analytics/model/model_123/confusion-matrix")
matrix = response.json()
print(f"Accuracy: {matrix['accuracy']}")
print(f"Precision: {matrix['precision']}")
print(f"Recall: {matrix['recall']}")
print(f"F1 Score: {matrix['f1_score']}")

# 4. Experiment Comparison
print("\n4. Comparing Experiments...")
response = requests.post(f"{BASE_URL}/analytics/experiments/compare", 
                        json=["exp_1", "exp_2", "exp_3"])
comparison = response.json()
print(f"Best Experiment: {comparison['best_experiment']}")
print("Metrics:")
for metric, values in comparison['metrics'].items():
    print(f"  {metric}: {values}")

# 5. Usage Analytics
print("\n5. Usage Analytics...")
response = requests.get(f"{BASE_URL}/analytics/usage/overview?time_range=week")
usage = response.json()
print(f"Total Users: {usage['total_users']}")
print(f"Active Users: {usage['active_users']}")
print(f"Total API Calls: {usage['total_api_calls']}")
print("Most Used Models:")
for model in usage['most_used_models']:
    print(f"  - {model['name']}: {model['calls']} calls")

# 6. Cost Analytics
print("\n6. Cost Analytics...")
response = requests.get(f"{BASE_URL}/analytics/cost/overview?time_range=month")
cost = response.json()
print(f"Total Cost: ${cost['total_cost']}")
print(f"Cost per Prediction: ${cost['cost_per_prediction']}")
print(f"Savings from AutoScale: ${cost['savings_from_autoscale']}")
print("Cost by Service:")
for service, amount in cost['cost_by_service'].items():
    print(f"  {service}: ${amount}")

# 7. Business Metrics
print("\n7. Business Metrics...")
response = requests.get(f"{BASE_URL}/analytics/business/overview?time_range=month")
business = response.json()
print(f"Marketplace Revenue: ${business['marketplace_revenue']}")
print(f"Total Deployments: {business['total_deployments']}")
print(f"Total Experiments: {business['total_experiments']}")
print("Top Sellers:")
for seller in business['top_sellers']:
    print(f"  {seller['user_id']}: ${seller['revenue']} ({seller['models_sold']} models)")

# 8. ROI Calculation
print("\n8. ROI Calculation...")
response = requests.get(f"{BASE_URL}/analytics/business/roi")
roi = response.json()
print(f"Total Investment: ${roi['total_investment']}")
print(f"Total Revenue: ${roi['total_revenue']}")
print(f"Net Profit: ${roi['net_profit']}")
print(f"ROI: {roi['roi_percentage']}%")
print(f"Payback Period: {roi['payback_period_months']} months")

# 9. Generate Report
print("\n9. Generating Report...")
response = requests.post(f"{BASE_URL}/analytics/reports/generate?report_type=monthly&time_range=month&format=pdf")
report = response.json()
print(f"Report ID: {report['report_id']}")
print(f"Format: {report['format']}")
print(f"Size: {report['size_kb']} KB")
print(f"Download URL: {report['download_url']}")

print("\n=== ANALYTICS SERVICE WORKS PERFECTLY! ===")
