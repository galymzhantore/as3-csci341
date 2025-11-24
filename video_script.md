=# Video Presentation Script: Online Caregivers Platform
**Course:** CSCI 341 - Database Management Systems  
**Assignment:** 3  
**Target Length:** ~8 minutes

---

## 0:00 - 0:30 | Introduction
**Visual:** Title slide with "Online Caregivers Platform", Course Name, and Team Members' Names.

**Speaker:**
"Hello everyone. This is our submission for Assignment 3, the Online Caregivers Platform. In this project, we designed and implemented a comprehensive database system for connecting families with professional caregivers.

Our project consists of three main parts:
1.  **Part 1:** Designing the database schema and creating the physical database using PostgreSQL.
2.  **Part 2:** Interacting with the database using Python and SQLAlchemy to perform complex queries and updates.
3.  **Part 3:** Developing a full-stack web application using Flask to demonstrate CRUD operations.

Let's dive into Part 1."

---

## 0:30 - 2:00 | Part 1: Database Design & Creation
**Visual:** Show the Entity-Relationship (ER) Diagram or the Schema Diagram. Then switch to the `caregivers_platform_part1.sql` file in an IDE (e.g., DataGrip or VS Code).

**Speaker:**
"For the first part, we designed a relational database schema to model the platform's requirements.

We started with a base `USER` table to store common attributes like email, name, and password. We then used **inheritance** to create two specialized tables: `CAREGIVER` and `MEMBER`.
-   The `CAREGIVER` table stores specific details like hourly rate, caregiving type (e.g., Babysitter, Elderly Care), and photo.
-   The `MEMBER` table stores house rules and descriptions of the dependent.

We also have tables for:
-   `ADDRESS`: Storing member addresses.
-   `JOB`: For job advertisements posted by members.
-   `JOB_APPLICATION`: A many-to-many link between caregivers and jobs.
-   `APPOINTMENT`: Managing the actual service bookings with status tracking.

**Visual:** Run the `caregivers_platform_part1.sql` script in the terminal or database tool. Show the output confirming table creation and data insertion.

**Speaker:**
"We implemented this schema using PostgreSQL. Here, you can see our SQL script `caregivers_platform_part1.sql`. It first drops any existing tables to ensure a clean slate, then creates all tables with appropriate Primary and Foreign Keys to maintain referential integrity.

We also populated the database with over 10 records per table to ensure we have enough data for testing. As you can see, the script executes successfully, creating the tables and inserting the sample data."

---

## 2:00 - 5:00 | Part 2: Database Interaction (SQLAlchemy)
**Visual:** Switch to `caregivers_platform_part2.py` in the IDE.

**Speaker:**
"Moving on to Part 2, we used Python and the **SQLAlchemy** library to interact with our database programmatically. We defined ORM models for each of our tables to map Python classes to database tables.

Let's look at the queries we implemented."

**Visual:** Run the python script `python3 caregivers_platform_part2.py`. Scroll through the output as you explain each section.

**Speaker:**
"**First, Updates:**
-   We updated 'Arman Armanov's' phone number. You can see the old and new values printed here.
-   We also implemented a logic to increase hourly rates: 10% for 'Elderly Care' in 'Astana' and 5% for everyone else. The output shows the rate changes for specific caregivers.

**Second, Deletions:**
-   We deleted all jobs posted by 'Amina Aminova'.
-   We also removed members living on 'Kabanbay Batyr' street. The script confirms the number of records deleted.

**Third, Simple Queries:**
-   We listed all 'accepted' appointments.
-   We searched for jobs requiring a 'soft-spoken' caregiver using a case-insensitive search.
-   We also filtered for Members in 'Astana' who have a 'No pets' rule.

**Fourth, Complex Queries:**
-   Here, we used **joins and aggregation**. This query counts the number of applicants for each job.
-   We also calculated the appointment count for each caregiver to see who is most active.
-   And we calculated the average hourly rate for each caregiving type.

**Finally, Derived Attributes and Views:**
-   We calculated the 'Total Revenue' from all accepted appointments by multiplying work hours with the hourly rate for each appointment.
-   We also created a database **VIEW** called `job_application_details` to simplify retrieving application data with caregiver names. You can see the sample data fetched from this view."

---

## 5:00 - 7:30 | Part 3: Web Application
**Visual:** Switch to the browser showing the running Flask application (http://127.0.0.1:5002).

**Speaker:**
"For the final part, we built a web application using **Flask**. This app provides a user-friendly interface to perform CRUD operations on our database.

**Visual:** Navigate to the 'Dashboard' page.
**Speaker:**
"Here is the **Dashboard**, which gives us a quick overview of the platform stats, like total users, active jobs, and accepted appointments."

**Visual:** Navigate to the 'Users' tab. Click 'Create User', fill in a form, and submit.
**Speaker:**
"Let's demonstrate **Creating** a user. I'll add a new user named 'John Doe'. After submitting, you can see John appears in the list."

**Visual:** Click 'Edit' on a user, change a detail, and save. Then click 'Delete' on a user.
**Speaker:**
"We can also **Edit** user details and **Delete** users directly from the interface."

**Visual:** Navigate to 'Jobs' and 'Appointments'.
**Speaker:**
"The same CRUD functionality exists for **Jobs** and **Appointments**.
-   Members can post new Jobs.
-   We can manage Appointments, linking a Caregiver to a Member and setting the status to 'pending' or 'accepted'.

The application uses the same SQLAlchemy models from Part 2, ensuring consistency across the project."

---

## 7:30 - 8:00 | Conclusion
**Visual:** Return to the Title Slide or a "Thank You" slide.

**Speaker:**
"In conclusion, this project allowed us to go from designing a conceptual database model to implementing a physical PostgreSQL database, interacting with it via Python scripts, and finally building a full web interface to manage the data.

We successfully met all the requirements for schema design, complex querying, and full-stack implementation.

Thank you for watching."
