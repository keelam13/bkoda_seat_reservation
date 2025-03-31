# Transportation Seat Reservation App - Features

## Application Pages

The application includes the following pages:

- Home page
- Login page
- Registration page
- Logout page
- Reset password page
- Trip Selection Page
- Reservation Form Page
- Reservation List Page (Passenger)
- Reservation List Page (Admin)
- Admin Trip Management Page

## Access to Pages by User Role

| Page Name                   | Passenger | Admin |
| --------------------------- | --------- | ----- |
| Home page                   | Y         | Y     |
| Login page                  | Y         | Y     |
| Registration page           | Y         | Y     |
| Logout page                 | Y         | Y     |
| Reset password page         | N         | Y     |
| Trip Selection Page         | Y         | N     |
| Reservation Form Page       | Y         | N     |
| Reservation List Page (Passenger) | Y   | Y     |
| Reservation List Page (Admin) | N       | Y     |
| Admin Trip Management Page | N         | Y     |

- Each page has a consistent navbar and footer.

## Navbar

- **Home page link:** Directs users to the application's homepage.
- **Login/Registration button:** Provides access to login and registration functionalities.
- **Logo:** Displays the application's logo.
- **My Reservation:** Displays the list of user's reservations.
- **Logout:** Logs user out of the application.

## Footer

- **Contact Information:** Includes relevant contact details (email and phone).
- **Social Media Account:** Links to the BKODA's social media accounts.
- **Responsive design:** Adapts to mobile and desktop views.

## Home Page

- **Welcome Message:** Greets users and provides a brief overview of the application.
- **"Get Started" Button:** Links to the registration page.
- **Benefits Section:** Highlights key features and advantages of using the application.
- **Call to Action:** Encourages users to sign up and begin booking.

## Registration Page

- **Sign-up Form:** Collects user information (email, username, first name, last name, phone number, password).
- **Form Validation:** Ensures correct data entry.
- **"Login" Link:** Redirects users to the login page.

## Login Page

- **Login Form:** Collects username/email and password.
- **"Sign In" Button:** Authenticates users and redirects them to the appropriate page.
- **"Forgot Password?" Link:** Redirects users to the password reset page.
- **"Sign Up" Link:** Redirects users to the registration page.

## Logout Page

- **Confirmation Message:** Asks users to confirm logout.
- **"Sign Out" Button:** Logs users out and redirects them to the home page.

## Forgot Password Page
Unfortunately coder was not able to accomplish this feature in time for the submission. But this will be included in the future improvements.

- **Password Reset Form:** Collects user's email address.
- **"Reset My Password" Button:** Sends a password reset link to the user's email.
- **Form Validation:** Checks for valid email format.

Instead, when the user clicks the Reset My Password button, a message will be displayed that the function is currently unavailable and to contact the admin for assistance.

## Trip Selection Page

- **Search Functionality:** Allows users to search for trips by origin, destination, and date.
- **Trip List:** Displays available trips with details (route, date, time, total seats).
- **Seat Availability:** Shows the number of available seats for each route.
- **Reserve Button:** Displays the Reservation Form Page

## Reservation Form Page

- **Seat Reservation:** Allows users to enter desired number of seats.
- **Form validation:** Checks the entered number of seat against the available seats, checks if the number entered is lower or equal to zero, and if the entered number of seat is greater than the total seats and raises an error.

## Reservation List Page (Passenger)

- **Reservation:** Displays a list of the user's past and upcoming reservations.
- **Reservation Details:** Allows users to view details of each reservation.
- **Update Reservation:** Allows users to change number of seat.
- **Cancel Reservation:** Allows users to cancel their booking.

## Reservation List Page (Admin)

- **All Reservation:** Displays a list of all reservations.
- **Reservation Details:** Allows admins to view details of each reservation.
- **Modify Reservation:** Allows admins to make changes to reservations.
- **Cancel Reservation:** Allows admins to cancel reservations.

## Admin Trip Management Page

- **Add Route:** Allows admins to add new trips.
- **Edit Route:** Allows admins to edit existing trip details (Route, date, time, seats).
- **Delete Route:** Allows admins to remove trips.

This document outlines the core features and functionalities of the Transportation Seat Reservation App.

* Trips search.
* Booking management (view, update seats, cancel).
* User authentication (registration, login).
* Admin panel for route, schedule, and seat management.
* Responsive design.