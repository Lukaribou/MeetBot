CREATE TABLE `profiles` (
	`user_id` VARCHAR(25) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`name` VARCHAR(40) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`gender` VARCHAR(15) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`description` TINYTEXT NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`age` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0',
	`country` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`other` VARCHAR(500) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`active` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1',
	`creation_date` TIMESTAMP NOT NULL DEFAULT current_timestamp(),
	`last_meet` TIMESTAMP NOT NULL DEFAULT current_timestamp(),
	`color` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT '0',
	INDEX `Index 1` (`user_id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
