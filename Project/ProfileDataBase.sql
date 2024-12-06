-- Use the database
USE profileData;

-- Drop the table if it already exists
IF OBJECT_ID('users', 'U') IS NOT NULL
    DROP TABLE users;

-- Create the users table
CREATE TABLE users (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    major VARCHAR(100)
);

-- Insert a sample user into the users table
INSERT INTO users (username, password, email, major)
VALUES ('exampleUser', 'hashedPassword', 'example@example.com', 'Computer Science');

-- Select a user from the users table
SELECT * FROM users WHERE username = 'exampleUser';

-- Update a user's email and major
UPDATE users
SET email = 'newemail@example.com', major = 'Finance'
WHERE username = 'exampleUser';

-- Delete a user from the users table
DELETE FROM users WHERE username = 'exampleUser';
