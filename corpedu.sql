-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 11, 2026 at 10:31 PM
-- Server version: 8.0.42
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `corpedu`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_feedbacksubmission`
--

CREATE TABLE `app_feedbacksubmission` (
  `id` bigint NOT NULL,
  `name` varchar(120) NOT NULL,
  `phone` varchar(40) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_knowledgetest`
--

CREATE TABLE `app_knowledgetest` (
  `id` bigint NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(280) NOT NULL,
  `summary` longtext NOT NULL,
  `estimated_minutes` int UNSIGNED NOT NULL,
  `passing_score_percent` smallint UNSIGNED NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `published_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `category_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_knowledgetest`
--

INSERT INTO `app_knowledgetest` (`id`, `title`, `slug`, `summary`, `estimated_minutes`, `passing_score_percent`, `is_published`, `published_at`, `created_at`, `updated_at`, `author_id`, `category_id`) VALUES
(2, 'Криптография', 'test', 'Короткий тест по Криптографии', 15, 80, 1, '2026-04-11 19:55:52.953945', '2026-04-11 19:49:36.643889', '2026-04-11 19:55:52.953945', 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `app_knowledgetestanswerchoice`
--

CREATE TABLE `app_knowledgetestanswerchoice` (
  `id` bigint NOT NULL,
  `order` int UNSIGNED NOT NULL,
  `text` longtext NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `question_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_knowledgetestanswerchoice`
--

INSERT INTO `app_knowledgetestanswerchoice` (`id`, `order`, `text`, `is_correct`, `question_id`) VALUES
(1, 1, 'Метод хранения данных', 0, 1),
(2, 2, 'Метод защиты информации путем шифрования', 1, 1),
(3, 3, 'Способ передачи данных', 0, 1),
(4, 4, 'Вид программирования', 0, 1),
(5, 1, 'Два разных ключа', 0, 2),
(6, 2, 'Один общий ключ', 1, 2),
(7, 3, 'Пароль и логин', 0, 2),
(8, 4, 'Только открытый ключ', 0, 2),
(9, 1, 'Шифрование с возможностью восстановления', 0, 3),
(10, 2, 'Сжатие данных', 0, 3),
(11, 3, 'Преобразование данных в фиксированную строку', 1, 3),
(12, 4, 'Передача данных', 0, 3),
(13, 1, 'Вид пароля', 0, 4),
(14, 2, 'Способ сжатия данных', 0, 4),
(15, 3, 'Метод подтверждения подлинности', 1, 4),
(16, 4, 'Тип вируса', 0, 4),
(17, 1, 'Ускорение интернета', 0, 5),
(18, 2, 'Защиту передачи данных', 1, 5),
(19, 3, 'Хранение данных', 0, 5),
(20, 4, 'Удаление вирусов', 0, 5);

-- --------------------------------------------------------

--
-- Table structure for table `app_knowledgetestattempt`
--

CREATE TABLE `app_knowledgetestattempt` (
  `id` bigint NOT NULL,
  `started_at` datetime(6) NOT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `score_percent` smallint UNSIGNED DEFAULT NULL,
  `is_passed` tinyint(1) DEFAULT NULL,
  `test_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_knowledgetestattempt`
--

INSERT INTO `app_knowledgetestattempt` (`id`, `started_at`, `completed_at`, `score_percent`, `is_passed`, `test_id`, `user_id`) VALUES
(1, '2026-04-11 20:01:15.814983', '2026-04-11 20:01:22.714169', 60, 0, 2, 1),
(2, '2026-04-11 20:01:26.008450', '2026-04-11 20:01:34.670282', 100, 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_knowledgetestattemptanswer`
--

CREATE TABLE `app_knowledgetestattemptanswer` (
  `id` bigint NOT NULL,
  `attempt_id` bigint NOT NULL,
  `selected_choice_id` bigint NOT NULL,
  `question_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_knowledgetestattemptanswer`
--

INSERT INTO `app_knowledgetestattemptanswer` (`id`, `attempt_id`, `selected_choice_id`, `question_id`) VALUES
(1, 1, 3, 1),
(2, 1, 7, 2),
(3, 1, 11, 3),
(4, 1, 15, 4),
(5, 1, 18, 5),
(6, 2, 2, 1),
(7, 2, 6, 2),
(8, 2, 11, 3),
(9, 2, 15, 4),
(10, 2, 18, 5);

-- --------------------------------------------------------

--
-- Table structure for table `app_knowledgetestquestion`
--

CREATE TABLE `app_knowledgetestquestion` (
  `id` bigint NOT NULL,
  `order` int UNSIGNED NOT NULL,
  `text` longtext NOT NULL,
  `test_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_knowledgetestquestion`
--

INSERT INTO `app_knowledgetestquestion` (`id`, `order`, `text`, `test_id`) VALUES
(1, 1, 'Что такое криптография?', 2),
(2, 2, 'Что используется в симметричном шифровании?', 2),
(3, 3, 'Какова основная функция хеширования?', 2),
(4, 4, 'Что такое цифровая подпись?', 2),
(5, 5, 'Что обеспечивает протокол SSL/TLS?', 2);

-- --------------------------------------------------------

--
-- Table structure for table `app_learningmaterial`
--

CREATE TABLE `app_learningmaterial` (
  `id` bigint NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(280) NOT NULL,
  `summary` longtext NOT NULL,
  `content` longtext NOT NULL,
  `material_format` varchar(20) NOT NULL,
  `estimated_minutes` int UNSIGNED NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `published_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `category_id` bigint NOT NULL,
  `attachment` varchar(100) DEFAULT NULL
) ;

--
-- Dumping data for table `app_learningmaterial`
--

INSERT INTO `app_learningmaterial` (`id`, `title`, `slug`, `summary`, `content`, `material_format`, `estimated_minutes`, `is_published`, `published_at`, `created_at`, `updated_at`, `author_id`, `category_id`, `attachment`) VALUES
(2, 'Введение в криптографию', 'material', 'Краткий учебный материал по криптографии, раскрывающий основные принципы защиты информации и методы шифрования', '', 'article', 10, 1, '2026-04-11 17:01:26.047316', '2026-04-11 17:01:26.050272', '2026-04-11 17:01:26.050272', 3, 3, 'materials/attachments/cryptography_training.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `app_materialcategory`
--

CREATE TABLE `app_materialcategory` (
  `id` bigint NOT NULL,
  `name` varchar(120) NOT NULL,
  `slug` varchar(140) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_materialcategory`
--

INSERT INTO `app_materialcategory` (`id`, `name`, `slug`, `description`, `created_at`, `updated_at`) VALUES
(1, 'Основы', 'category', 'Введение в ИБ\r\nОсновные термины и принципы (CIA triad: конфиденциальность, целостность, доступность)\r\nМодели угроз и рисков\r\nПолитики безопасности', '2026-04-09 12:51:58.484632', '2026-04-09 12:51:58.484632'),
(2, 'Сетевая безопасность', 'category-2', 'Протоколы (TCP/IP, HTTPS, VPN)\r\nМежсетевые экраны (firewalls)\r\nIDS/IPS системы\r\nЗащита сетевой инфраструктуры', '2026-04-09 12:52:15.621322', '2026-04-09 12:52:15.621322'),
(3, 'Криптография', 'category-3', 'Симметричное и асимметричное шифрование\r\nХэш-функции\r\nЦифровые подписи\r\nPKI (инфраструктура открытых ключей)', '2026-04-09 12:52:31.440904', '2026-04-09 12:57:27.934190'),
(4, 'Безопасность приложений', 'category-4', 'OWASP Top 10\r\nУязвимости (SQL-инъекции, XSS и др.)\r\nSecure coding practices\r\nТестирование безопасности ПО', '2026-04-09 12:57:47.939876', '2026-04-09 12:57:47.939876'),
(5, 'Операционная безопасность', 'category-5', 'Управление доступом (IAM)\r\nКонтроль пользователей\r\nЛогирование и мониторинг\r\nИнцидент-менеджмент', '2026-04-09 12:57:57.099796', '2026-04-09 12:57:57.099796'),
(6, 'Безопасность операционных систем', 'category-6', 'Windows / Linux hardening\r\nКонтроль процессов\r\nУправление правами\r\nОбновления и патчи', '2026-04-09 12:58:12.942353', '2026-04-09 12:58:12.942353');

-- --------------------------------------------------------

--
-- Table structure for table `app_materialpage`
--

CREATE TABLE `app_materialpage` (
  `id` int NOT NULL,
  `order` int UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `quiz_question` longtext NOT NULL,
  `quiz_choice_1` longtext NOT NULL,
  `quiz_choice_2` longtext NOT NULL,
  `quiz_choice_3` longtext NOT NULL,
  `quiz_choice_4` longtext NOT NULL,
  `quiz_correct` smallint UNSIGNED DEFAULT NULL,
  `material_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_materialpage`
--

INSERT INTO `app_materialpage` (`id`, `order`, `title`, `body`, `image`, `quiz_question`, `quiz_choice_1`, `quiz_choice_2`, `quiz_choice_3`, `quiz_choice_4`, `quiz_correct`, `material_id`) VALUES
(2, 0, 'Введение в криптографию', 'Криптография — это метод защиты информации путем её преобразования в недоступный для посторонних вид. Она используется для обеспечения безопасности данных при хранении и передаче.\r\n\r\nОсновные цели криптографии:\r\n\r\nКонфиденциальность — защита информации от посторонних\r\nЦелостность — предотвращение изменения данных\r\nАутентификация — подтверждение подлинности отправителя\r\nНеотказуемость — невозможность отрицания факта отправки\r\n\r\nОсновные виды шифрования:\r\n\r\nСимметричное шифрование — используется один ключ для шифрования и расшифровки (например, AES)\r\nАсимметричное шифрование — используются два ключа: открытый и закрытый (например, RSA)\r\n\r\nПримеры применения:\r\n\r\nЗащита паролей\r\nОнлайн-банкинг\r\nVPN и защищённые соединения (HTTPS)', 'materials/pages/cryptograph_p1.jpg', 'Что означает принцип конфиденциальности?', 'Данные всегда доступны', 'Данные защищены от несанкционированного доступа', 'Данные можно изменять', 'Данные удаляются автоматически', 2, 2),
(3, 1, 'Практическое применение криптографии', 'В корпоративной среде криптография применяется ежедневно, даже если сотрудники этого не замечают.\r\n\r\nОсновные инструменты:\r\n\r\nSSL/TLS — защищает передачу данных в интернете\r\nХеширование — преобразует данные в уникальную строку фиксированной длины (например, SHA-256)\r\nЦифровая подпись — подтверждает подлинность документов\r\n\r\nРекомендации для сотрудников:\r\n\r\nИспользуйте сложные пароли и не передавайте их третьим лицам\r\nПроверяйте наличие защищённого соединения (значок замка в браузере)\r\nНе открывайте подозрительные файлы и ссылки\r\nИспользуйте двухфакторную аутентификацию (2FA)\r\n\r\nПочему это важно:\r\nДаже самый надёжный алгоритм не защитит систему, если сотрудники игнорируют базовые правила безопасности.', 'materials/pages/cryptograph_p2.jpg', 'Что делает хеширование?', 'Шифрует данные с возможностью обратного восстановления', 'Удаляет данные', 'Преобразует данные в уникальную фиксированную строку', 'Передаёт данные по сети', 3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `app_user`
--

CREATE TABLE `app_user` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_user`
--

INSERT INTO `app_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `created_at`, `updated_at`) VALUES
(1, 'pbkdf2_sha256$1200000$dYUnvhUTRzgPpmdPOBkVep$gs22wgFo13sCoNS14dPSgBGDegWInzaPp84CUfqoY/8=', '2026-04-11 22:19:53.489668', 0, 'user', 'Пользователь', 'Тестовый', '', 0, 1, '2026-04-09 09:55:47.125268', 'user', '2026-04-09 09:55:48.150263', '2026-04-09 09:55:48.150263'),
(2, 'pbkdf2_sha256$1200000$Vi6QOeYNea7xq1LnFsa1Gm$N3yo55sAMYvclrvCtsrtKckDKQ9gfQ+qF+9QUfJsD+w=', '2026-04-11 22:22:01.272783', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2026-04-09 12:23:19.906719', 'administrator', '2026-04-09 12:23:20.870174', '2026-04-09 12:23:20.870174'),
(3, 'pbkdf2_sha256$1200000$yegxasR41SmgM2peZH7fdV$u5biW8OKzQZUc4OS6t9jx+hQdjYEgwT+dqBLXaKq4RE=', '2026-04-11 22:19:14.830241', 0, 'kurator', 'Куратор', 'Тестовый', '', 0, 1, '2026-04-09 12:38:31.895626', 'curator', '2026-04-09 12:38:33.044223', '2026-04-09 12:38:33.044223');

-- --------------------------------------------------------

--
-- Table structure for table `app_usermaterialpagequizcompletion`
--

CREATE TABLE `app_usermaterialpagequizcompletion` (
  `id` bigint NOT NULL,
  `selected_choice` smallint UNSIGNED NOT NULL,
  `completed_at` datetime(6) NOT NULL,
  `page_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_usermaterialpagequizcompletion`
--

INSERT INTO `app_usermaterialpagequizcompletion` (`id`, `selected_choice`, `completed_at`, `page_id`, `user_id`) VALUES
(1, 2, '2026-04-11 17:16:18.744069', 2, 1),
(2, 3, '2026-04-11 17:16:59.772532', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_usermaterialprogress`
--

CREATE TABLE `app_usermaterialprogress` (
  `id` bigint NOT NULL,
  `last_page_index` int UNSIGNED NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `material_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_usermaterialprogress`
--

INSERT INTO `app_usermaterialprogress` (`id`, `last_page_index`, `updated_at`, `material_id`, `user_id`) VALUES
(1, 1, '2026-04-11 17:15:21.004877', 2, 3),
(2, 1, '2026-04-11 17:17:15.284411', 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_user_groups`
--

CREATE TABLE `app_user_groups` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_user_user_permissions`
--

CREATE TABLE `app_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add Пользователь', 1, 'add_user'),
(2, 'Can change Пользователь', 1, 'change_user'),
(3, 'Can delete Пользователь', 1, 'delete_user'),
(4, 'Can view Пользователь', 1, 'view_user'),
(5, 'Can add log entry', 2, 'add_logentry'),
(6, 'Can change log entry', 2, 'change_logentry'),
(7, 'Can delete log entry', 2, 'delete_logentry'),
(8, 'Can view log entry', 2, 'view_logentry'),
(9, 'Can add permission', 4, 'add_permission'),
(10, 'Can change permission', 4, 'change_permission'),
(11, 'Can delete permission', 4, 'delete_permission'),
(12, 'Can view permission', 4, 'view_permission'),
(13, 'Can add group', 3, 'add_group'),
(14, 'Can change group', 3, 'change_group'),
(15, 'Can delete group', 3, 'delete_group'),
(16, 'Can view group', 3, 'view_group'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Категория материала', 8, 'add_materialcategory'),
(26, 'Can change Категория материала', 8, 'change_materialcategory'),
(27, 'Can delete Категория материала', 8, 'delete_materialcategory'),
(28, 'Can view Категория материала', 8, 'view_materialcategory'),
(29, 'Can add Обучающий материал', 7, 'add_learningmaterial'),
(30, 'Can change Обучающий материал', 7, 'change_learningmaterial'),
(31, 'Can delete Обучающий материал', 7, 'delete_learningmaterial'),
(32, 'Can view Обучающий материал', 7, 'view_learningmaterial'),
(33, 'Can add Страница материала', 9, 'add_materialpage'),
(34, 'Can change Страница материала', 9, 'change_materialpage'),
(35, 'Can delete Страница материала', 9, 'delete_materialpage'),
(36, 'Can view Страница материала', 9, 'view_materialpage'),
(37, 'Can add Пройденный тест страницы', 10, 'add_usermaterialpagequizcompletion'),
(38, 'Can change Пройденный тест страницы', 10, 'change_usermaterialpagequizcompletion'),
(39, 'Can delete Пройденный тест страницы', 10, 'delete_usermaterialpagequizcompletion'),
(40, 'Can view Пройденный тест страницы', 10, 'view_usermaterialpagequizcompletion'),
(41, 'Can add Прогресс по материалу', 11, 'add_usermaterialprogress'),
(42, 'Can change Прогресс по материалу', 11, 'change_usermaterialprogress'),
(43, 'Can delete Прогресс по материалу', 11, 'delete_usermaterialprogress'),
(44, 'Can view Прогресс по материалу', 11, 'view_usermaterialprogress'),
(45, 'Can add Тест', 12, 'add_knowledgetest'),
(46, 'Can change Тест', 12, 'change_knowledgetest'),
(47, 'Can delete Тест', 12, 'delete_knowledgetest'),
(48, 'Can view Тест', 12, 'view_knowledgetest'),
(49, 'Can add Попытка теста', 14, 'add_knowledgetestattempt'),
(50, 'Can change Попытка теста', 14, 'change_knowledgetestattempt'),
(51, 'Can delete Попытка теста', 14, 'delete_knowledgetestattempt'),
(52, 'Can view Попытка теста', 14, 'view_knowledgetestattempt'),
(53, 'Can add Вопрос теста', 16, 'add_knowledgetestquestion'),
(54, 'Can change Вопрос теста', 16, 'change_knowledgetestquestion'),
(55, 'Can delete Вопрос теста', 16, 'delete_knowledgetestquestion'),
(56, 'Can view Вопрос теста', 16, 'view_knowledgetestquestion'),
(57, 'Can add Вариант ответа (тест)', 13, 'add_knowledgetestanswerchoice'),
(58, 'Can change Вариант ответа (тест)', 13, 'change_knowledgetestanswerchoice'),
(59, 'Can delete Вариант ответа (тест)', 13, 'delete_knowledgetestanswerchoice'),
(60, 'Can view Вариант ответа (тест)', 13, 'view_knowledgetestanswerchoice'),
(61, 'Can add Ответ в попытке теста', 15, 'add_knowledgetestattemptanswer'),
(62, 'Can change Ответ в попытке теста', 15, 'change_knowledgetestattemptanswer'),
(63, 'Can delete Ответ в попытке теста', 15, 'delete_knowledgetestattemptanswer'),
(64, 'Can view Ответ в попытке теста', 15, 'view_knowledgetestattemptanswer'),
(65, 'Can add Обращение (обратная связь)', 17, 'add_feedbacksubmission'),
(66, 'Can change Обращение (обратная связь)', 17, 'change_feedbacksubmission'),
(67, 'Can delete Обращение (обратная связь)', 17, 'delete_feedbacksubmission'),
(68, 'Can view Обращение (обратная связь)', 17, 'view_feedbacksubmission');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(2, 'admin', 'logentry'),
(17, 'app', 'feedbacksubmission'),
(12, 'app', 'knowledgetest'),
(13, 'app', 'knowledgetestanswerchoice'),
(14, 'app', 'knowledgetestattempt'),
(15, 'app', 'knowledgetestattemptanswer'),
(16, 'app', 'knowledgetestquestion'),
(7, 'app', 'learningmaterial'),
(8, 'app', 'materialcategory'),
(9, 'app', 'materialpage'),
(1, 'app', 'user'),
(10, 'app', 'usermaterialpagequizcompletion'),
(11, 'app', 'usermaterialprogress'),
(3, 'auth', 'group'),
(4, 'auth', 'permission'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-04-09 09:49:53.503545'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-04-09 09:49:54.921200'),
(3, 'auth', '0001_initial', '2026-04-09 09:49:58.025656'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-04-09 09:49:58.728187'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-04-09 09:49:58.754798'),
(6, 'auth', '0004_alter_user_username_opts', '2026-04-09 09:49:58.801799'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-04-09 09:49:58.853327'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-04-09 09:49:58.894327'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-04-09 09:49:58.926325'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-04-09 09:49:58.962895'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-04-09 09:49:58.996894'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-04-09 09:49:59.689102'),
(13, 'auth', '0011_update_proxy_permissions', '2026-04-09 09:49:59.733107'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-04-09 09:49:59.762621'),
(15, 'app', '0001_initial', '2026-04-09 09:50:03.524090'),
(16, 'admin', '0001_initial', '2026-04-09 09:50:05.319001'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-04-09 09:50:05.362581'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-04-09 09:50:05.407644'),
(19, 'sessions', '0001_initial', '2026-04-09 09:50:05.849961'),
(20, 'app', '0002_alter_user_role', '2026-04-09 09:53:54.484661'),
(21, 'app', '0003_materialcategory_learningmaterial', '2026-04-09 12:20:00.207386'),
(22, 'app', '0004_learningmaterial_attachment', '2026-04-09 13:20:32.740567'),
(23, 'app', '0005_material_pages', '2026-04-10 20:26:06.766774'),
(24, 'app', '0005_alter_learningmaterial_content_materialpage', '2026-04-10 21:13:26.646759'),
(25, 'app', '0006_user_material_progress', '2026-04-11 17:13:58.174294'),
(26, 'app', '0007_alter_usermaterialpagequizcompletion_id_and_more', '2026-04-11 18:02:32.195436'),
(27, 'app', '0008_feedback_submission', '2026-04-11 20:24:47.206414'),
(28, 'app', '0009_alter_feedbacksubmission_id', '2026-04-11 20:24:48.034307');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('37xhj9j0k99xz3dc4m4lv3kjcpbnlu7x', '.eJxVjMsOwiAQRf-FtSFQ3i7d-w1kYAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKM7MwmdvrdEuQHtR3gHdqt89zbusyJ7wo_6ODXjvS8HO7fQYVRv7W2SU3K2BJQOI-pqAxJoStU0CuNYDUaEibljCFYClI5YZ2U3ktfXGDvD_dUN_M:1wBgiH:8HdAxPZch5T8NpEd2AlTBtS2F3VPQP8pF28FKUl6XXA', '2026-04-25 22:22:01.314744'),
('di0hoaahlxc53g1mb2ootx9vswnqudtw', '.eJxVjMsOwiAQRf-FtSFQ3i7d-w1kYAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKM7MwmdvrdEuQHtR3gHdqt89zbusyJ7wo_6ODXjvS8HO7fQYVRv7W2SU3K2BJQOI-pqAxJoStU0CuNYDUaEibljCFYClI5YZ2U3ktfXGDvD_dUN_M:1wBgfG:itwmJ_upSq2eZ9QrFEeo64OS7t3e-x8Iyn34ctw7Bt4', '2026-04-25 22:18:54.844939');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_feedbacksubmission`
--
ALTER TABLE `app_feedbacksubmission`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_feedbacksubmission_user_id_606bffc3_fk_app_user_id` (`user_id`),
  ADD KEY `app_feedbacksubmission_status_d98b1bd8` (`status`);

--
-- Indexes for table `app_knowledgetest`
--
ALTER TABLE `app_knowledgetest`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `app_knowledgetest_author_id_3854033c_fk_app_user_id` (`author_id`),
  ADD KEY `app_knowledgetest_category_id_cd68a041_fk_app_mater` (`category_id`);

--
-- Indexes for table `app_knowledgetestanswerchoice`
--
ALTER TABLE `app_knowledgetestanswerchoice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_knowledgetestans_question_id_26ef6134_fk_app_knowl` (`question_id`);

--
-- Indexes for table `app_knowledgetestattempt`
--
ALTER TABLE `app_knowledgetestattempt`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_knowledgetestatt_test_id_95ac4434_fk_app_knowl` (`test_id`),
  ADD KEY `app_knowledgetestattempt_user_id_59acc7c8_fk_app_user_id` (`user_id`);

--
-- Indexes for table `app_knowledgetestattemptanswer`
--
ALTER TABLE `app_knowledgetestattemptanswer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_knowledge_test_attempt_question` (`attempt_id`,`question_id`),
  ADD KEY `app_knowledgetestatt_selected_choice_id_7eb6ce31_fk_app_knowl` (`selected_choice_id`),
  ADD KEY `app_knowledgetestatt_question_id_b270c6c2_fk_app_knowl` (`question_id`);

--
-- Indexes for table `app_knowledgetestquestion`
--
ALTER TABLE `app_knowledgetestquestion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_knowledgetestque_test_id_17810373_fk_app_knowl` (`test_id`);

--
-- Indexes for table `app_learningmaterial`
--
ALTER TABLE `app_learningmaterial`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `app_learningmaterial_author_id_6478292e_fk_app_user_id` (`author_id`),
  ADD KEY `app_learningmaterial_category_id_a4cf4e9d_fk_app_mater` (`category_id`);

--
-- Indexes for table `app_materialcategory`
--
ALTER TABLE `app_materialcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `app_materialpage`
--
ALTER TABLE `app_materialpage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_materialpage_material_id_b8935253_fk_app_learningmaterial_id` (`material_id`);

--
-- Indexes for table `app_user`
--
ALTER TABLE `app_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `app_usermaterialpagequizcompletion`
--
ALTER TABLE `app_usermaterialpagequizcompletion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_user_page_quiz_completion` (`user_id`,`page_id`);

--
-- Indexes for table `app_usermaterialprogress`
--
ALTER TABLE `app_usermaterialprogress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_user_material_progress` (`user_id`,`material_id`);

--
-- Indexes for table `app_user_groups`
--
ALTER TABLE `app_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_user_groups_user_id_group_id_73b8e940_uniq` (`user_id`,`group_id`),
  ADD KEY `app_user_groups_group_id_e774d92c_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `app_user_user_permissions`
--
ALTER TABLE `app_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_user_user_permissions_user_id_permission_id_7c8316ce_uniq` (`user_id`,`permission_id`),
  ADD KEY `app_user_user_permis_permission_id_4ef8e133_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_app_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_feedbacksubmission`
--
ALTER TABLE `app_feedbacksubmission`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `app_knowledgetest`
--
ALTER TABLE `app_knowledgetest`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_knowledgetestanswerchoice`
--
ALTER TABLE `app_knowledgetestanswerchoice`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_knowledgetestattempt`
--
ALTER TABLE `app_knowledgetestattempt`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_knowledgetestattemptanswer`
--
ALTER TABLE `app_knowledgetestattemptanswer`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `app_knowledgetestquestion`
--
ALTER TABLE `app_knowledgetestquestion`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_learningmaterial`
--
ALTER TABLE `app_learningmaterial`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_materialcategory`
--
ALTER TABLE `app_materialcategory`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `app_materialpage`
--
ALTER TABLE `app_materialpage`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_user`
--
ALTER TABLE `app_user`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `app_usermaterialpagequizcompletion`
--
ALTER TABLE `app_usermaterialpagequizcompletion`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_usermaterialprogress`
--
ALTER TABLE `app_usermaterialprogress`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_user_groups`
--
ALTER TABLE `app_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_user_user_permissions`
--
ALTER TABLE `app_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `app_feedbacksubmission`
--
ALTER TABLE `app_feedbacksubmission`
  ADD CONSTRAINT `app_feedbacksubmission_user_id_606bffc3_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_knowledgetest`
--
ALTER TABLE `app_knowledgetest`
  ADD CONSTRAINT `app_knowledgetest_author_id_3854033c_fk_app_user_id` FOREIGN KEY (`author_id`) REFERENCES `app_user` (`id`),
  ADD CONSTRAINT `app_knowledgetest_category_id_cd68a041_fk_app_mater` FOREIGN KEY (`category_id`) REFERENCES `app_materialcategory` (`id`);

--
-- Constraints for table `app_knowledgetestanswerchoice`
--
ALTER TABLE `app_knowledgetestanswerchoice`
  ADD CONSTRAINT `app_knowledgetestans_question_id_26ef6134_fk_app_knowl` FOREIGN KEY (`question_id`) REFERENCES `app_knowledgetestquestion` (`id`);

--
-- Constraints for table `app_knowledgetestattempt`
--
ALTER TABLE `app_knowledgetestattempt`
  ADD CONSTRAINT `app_knowledgetestatt_test_id_95ac4434_fk_app_knowl` FOREIGN KEY (`test_id`) REFERENCES `app_knowledgetest` (`id`),
  ADD CONSTRAINT `app_knowledgetestattempt_user_id_59acc7c8_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_knowledgetestattemptanswer`
--
ALTER TABLE `app_knowledgetestattemptanswer`
  ADD CONSTRAINT `app_knowledgetestatt_attempt_id_ac20d2d6_fk_app_knowl` FOREIGN KEY (`attempt_id`) REFERENCES `app_knowledgetestattempt` (`id`),
  ADD CONSTRAINT `app_knowledgetestatt_question_id_b270c6c2_fk_app_knowl` FOREIGN KEY (`question_id`) REFERENCES `app_knowledgetestquestion` (`id`),
  ADD CONSTRAINT `app_knowledgetestatt_selected_choice_id_7eb6ce31_fk_app_knowl` FOREIGN KEY (`selected_choice_id`) REFERENCES `app_knowledgetestanswerchoice` (`id`);

--
-- Constraints for table `app_knowledgetestquestion`
--
ALTER TABLE `app_knowledgetestquestion`
  ADD CONSTRAINT `app_knowledgetestque_test_id_17810373_fk_app_knowl` FOREIGN KEY (`test_id`) REFERENCES `app_knowledgetest` (`id`);

--
-- Constraints for table `app_learningmaterial`
--
ALTER TABLE `app_learningmaterial`
  ADD CONSTRAINT `app_learningmaterial_author_id_6478292e_fk_app_user_id` FOREIGN KEY (`author_id`) REFERENCES `app_user` (`id`),
  ADD CONSTRAINT `app_learningmaterial_category_id_a4cf4e9d_fk_app_mater` FOREIGN KEY (`category_id`) REFERENCES `app_materialcategory` (`id`);

--
-- Constraints for table `app_materialpage`
--
ALTER TABLE `app_materialpage`
  ADD CONSTRAINT `app_materialpage_material_id_b8935253_fk_app_learningmaterial_id` FOREIGN KEY (`material_id`) REFERENCES `app_learningmaterial` (`id`);

--
-- Constraints for table `app_user_groups`
--
ALTER TABLE `app_user_groups`
  ADD CONSTRAINT `app_user_groups_group_id_e774d92c_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `app_user_groups_user_id_e6f878f6_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_user_user_permissions`
--
ALTER TABLE `app_user_user_permissions`
  ADD CONSTRAINT `app_user_user_permis_permission_id_4ef8e133_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `app_user_user_permissions_user_id_24780b52_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
