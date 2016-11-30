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
						.error(function(err, error_code) {
							if (error_code == 401 || error_code == 403 || error_code == 400 || error_code == 500) {
								$mdLoginToast.show('Invalid Login');
							} else if (error_code == -1){
								$mdLoginToast.show('Backend Server Unavailable');
							}
						});
				}
				if ($scope.loginForm.$invalid) {
					console.log("invalid");
				}
			};
		}]);
}
