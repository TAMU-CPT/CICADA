let jwt_decode = require("jwt-decode");

/**
 * Login Controller
 * @param {object} base Base angular application object
 */
export default function(base) {
	base.controller("LoginCtrl", ["$scope", "$http", "$localStorage", "$location", "$mdLoginToast", "DRF_URL",
		function($scope, $http, $localStorage, $location, $mdLoginToast, DRF_URL) {
			$scope.userData = {};

			$scope.saveData = function() {
				if ($scope.loginForm.$valid) {
					$http.post(DRF_URL + "api-token-auth/", $scope.userData)
						.success(function(data) {
							$localStorage.jwtToken = data.token;
							$localStorage.jwtData = jwt_decode(data.token);
							$scope.nav.userData = $localStorage.jwtData;
							$mdLoginToast.show("Success");
							$location.path("/");
						})
						.error(function() {
							$mdLoginToast.show("Invalid Login");
						});
				}
				if ($scope.loginForm.$invalid) {
					console.log("invalid");
				}
			};
		}]);
}
