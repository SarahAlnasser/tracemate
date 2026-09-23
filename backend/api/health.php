<?php
// Week 1 test: is the backend up and can it read the database?
require __DIR__ . '/../db.php';

try {
    $n = db()->query('SELECT COUNT(*) AS n FROM letter_templates')->fetch()['n'];
    json_response(['ok' => true, 'letter_templates' => (int)$n]);
} catch (Throwable $e) {
    json_response(['ok' => false, 'error' => $e->getMessage()], 500);
}
