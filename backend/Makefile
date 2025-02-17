.PHONY: helpers
helpers:
	php artisan ide-helper:generate
	php artisan ide-helper:models -F helpers/ModelHelper.php -M
	@# php artisan ide-helper:meta

.PHONY: analyse
analyse:
	./vendor/bin/phpstan analyse --memory-limit=2G