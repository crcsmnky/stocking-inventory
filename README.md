# Proactively Stocking Inventory using ML

## Background

How do you notify store associates when items are out of stock? What if you could leverage footage from in-store cameras to detect when stock is low for items that have a quick turnover (like produce) and have those refilled before running out? In this session, we’ll walk through an architecture that describes how to combine camera footage, the Cloud Vision API, and Firebase to deliver an end-to-end use case to help shoppers get the products they need without having to wait.

## Tasks

- Sample images uploaded to Cloud Storage
- Cloud Storage bucket notification to Cloud Pub/Sub
- Cloud Pub/Sub push to App Engine app, to analyze image
- Based on Vision API response, send message to Pub/Sub
- Cloud Pub/Sub push to App Engine app to send device notification
- Firebase delivers push notification
