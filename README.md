# Donation Campaigns Platform

A donation platform built with Django and PostgreSQL that presents campaigns as posts and lets users donate to them through a shopping cart style flow

## Overview

This project allows users to create donation campaigns as posts with a title description image or video target amount and a start and end time Other users can browse these campaigns add the ones they want to support to a cart choose how much to donate for each one and then confirm the donation at checkout There is also a page that ranks the top donors

## Features

- User signup and login with phone number validation
- Create edit and delete donation campaigns as posts
- Support for a campaign image upload or an external image link
- Support for an optional YouTube video link on a campaign
- Campaign start and end time to control when donations are open
- Search campaigns by title and by creation date
- Cart system where users add campaigns and set a custom donation amount for each
- Checkout flow that converts cart items into donations and updates the campaign progress
- Top donors page that ranks users by their total donation amount
- About page

## Project Structure

- donation_project contains the Django project settings urls and configuration
- donations is the main app containing models views forms urls templates and static files
- media folder stores uploaded campaign images
- donations/templates contains all the HTML pages including base templates for the main site and for authentication pages

## How It Works

### Models

- UserProfile extends the built in Django User with an Egyptian mobile phone number
- Post represents a donation campaign with a title description image or video target amount current amount and a start and end time
- Donation represents a single donation made by a user to a specific post
- Cart represents a user shopping cart
- CartItem represents a campaign added to the cart along with the chosen donation amount

### Views

- Authentication views handle signup login and logout
- Campaign views handle listing viewing creating editing deleting and searching posts
- Cart views handle adding removing and clearing items and updating the donation amount for each item
- The checkout view turns the cart items into donation records updates the campaign current amount and clears the cart
- The top donors view aggregates all donations per user and displays them ranked by total amount

### Forms

- SimpleSignupForm validates the signup fields including username format name format and Egyptian phone number format
- PostForm handles creating and editing campaigns including the image upload the optional video link and the start and end time fields

## Usage

### Requirements

- Python 3
- Django
- PostgreSQL

### Running the Project

1. Create a PostgreSQL database and update the database settings in donation_project settings.py if needed
2. Install the required packages
3. Run database migrations using manage.py migrate
4. Run the development server using manage.py runserver
5. Open the application in the browser at the local address shown in the terminal

## Notes

This project was built for learning purposes to practice Django models views forms authentication and building a small e commerce style flow around donations.

 