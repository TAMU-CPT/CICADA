window._ = require("lodash");
require("angular");
require("angular-route");
require("restangular");
require("angular-resource");
require("angular-material");
require("angular-material-icons");
require("angular-aria");
require("angular-gravatar");
require("angular-material-data-table");
require("angular-messages");
require("angular-animate");
require("jquery");
require("ngstorage");
require("angular-jwt");
// let moment = require("moment");

let {{cookiecutter.app_name}} = angular.module("{{cookiecutter.app_name}}", [
	"ngRoute",
	"restangular",
	"ngMdIcons",
	"ngMaterial",
	"ui.gravatar",
	"ngMessages",
	"ngAnimate",
	"md.data.table",
	"ngStorage", // https://github.com/gsklee/ngStorage
]);

{{cookiecutter.app_name}}.config(["$routeProvider", "$httpProvider", "$mdThemingProvider", "gravatarServiceProvider", "RestangularProvider", "DRF_URL",
	function($routeProvider, $httpProvider, $mdThemingProvider, gravatarServiceProvider, RestangularProvider, DRF_URL) {
		gravatarServiceProvider.defaults = {
			"size": 100,
			"default": "mm",  // Mystery man as default for missing avatars
		};
		gravatarServiceProvider.secure = true;
		gravatarServiceProvider.protocol = "my-protocol";
		$mdThemingProvider.theme("default")
			.primaryPalette("blue")
			.accentPalette("pink");
		$routeProvider.
// LOAD ROUTES
			when("/login", {
				templateUrl: "partials/login.html",
				controller: "LoginCtrl",
			}).
			when("/logout", {
				templateUrl: "partials/login.html",
				controller: "LogOutCtrl",
				resolve: {
					loginRequired: loginRequired,
				},
			}).
			when("/", {
				templateUrl: "partials/home.html",
				controller: "HomeCtrl",
			}).
			otherwise({
				redirectTo: "/",
			});

		/**
		 * loginRequired is a convenience function to ensure a user is logged
		 * in before accessing a route. This is not a security measure but a UX
		 * one. Security must be enforced on the backend
		 * @param {object} $q The promise resolution object
		 * @param {object} $location The location object
		 * @param {object} $localStorage The local storage access object
		 * @return {object} promise The promise
		 */
		function loginRequired($q, $location, $localStorage) {
			let deferred = $q.defer();
			if ($localStorage.jwtToken) {
				deferred.resolve();
			} else {
				$location.path("/login");
			}
			return deferred.promise;
		};

		RestangularProvider.setBaseUrl(DRF_URL);
		RestangularProvider.setRequestSuffix("/");
		RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
			let extractedData;
			// .. to look for getList operations
			if (operation === "getList") {
			// .. and handle the data and meta data
				extractedData = data.results;
				extractedData.meta = {
					"count": data.count,
					"next": data.next,
					"previous": data.previous,
				};
			} else {
				extractedData = data;
			}
			return extractedData;
		});

		$httpProvider.interceptors.push(["$q", "$location", "$localStorage", function($q, $location, $localStorage) {
			return {
				"request": function(config) {
					config.headers = config.headers || {};
					if ($localStorage.jwtToken) {
						config.headers.Authorization = "JWT " + $localStorage.jwtToken;
					}
					return config;
				},
				"responseError": function(response) {
					console.log("Failed with", response.status, "status");
					if (response.status == 401 || response.status == 403 || response.status == 400 || response.status == 500) {
						console.log("bad");
						// $location.path('/login');
					}
					return $q.reject(response);
				},
			};
		}]);
	}]);

require("./directives.js")(base);
require("./factory.js")(base);
require("./filter.js")(base);
require("./service.js")(base);
require("./const.js")(base);
require("./ctrl/home.js")(base);
require("./ctrl/nav.js")(base);
require("./ctrl/login.js")(base);
require("./ctrl/logout.js")(base);
// REQUIRE
