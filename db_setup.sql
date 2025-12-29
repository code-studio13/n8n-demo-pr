CREATE DATABASE IF NOT EXISTS `drone_pilot_db`;

USE `drone_pilot_db`;   

CREATE TABLE `applications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `full_name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE, -- Primary Key/Unique Constraint
    `country_code` VARCHAR(10),
    `phone_number` VARCHAR(50),
    `living_eu_uk` VARCHAR(5) NOT NULL,
    `hold_license` VARCHAR(5) NOT NULL,
    `prior_experience` VARCHAR(255),
    `own_drone_radio` VARCHAR(5) NOT NULL,
    `own_drone` VARCHAR(255),
    `willing_to_travel` VARCHAR(5) NOT NULL,
    `self_sponsor_invest` VARCHAR(5) NOT NULL,
    `submission_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- Note: Files (CV, License) are generally stored as paths or blobs, but for this exercise,
    -- we only store the metadata as the client-side form handles the file upload simulation.
);  