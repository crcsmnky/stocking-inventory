# Proactively Stocking Inventory using ML

## Background

How do you notify store associates when items are out of stock? What if you could leverage footage from in-store cameras to detect when stock is low for items that have a quick turnover (like produce) and have those refilled before running out? In this session, we’ll walk through an architecture that describes how to combine in-store camera footage, the Cloud Video Intelligence API, and Firebase to deliver an end-to-end use case to help shoppers get the products they need without having to wait.

## Tasks

- IP Camera mounted over bowl
- SBC uploads sampled images to Cloud Storage
- Firebase Functions runs image through Vision API
- Based on Vision API response, fire message
- Firebase delivers push notification
