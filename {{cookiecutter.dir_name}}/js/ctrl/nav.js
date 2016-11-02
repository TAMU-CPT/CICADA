/**
 * Nav menu controller
 * @param {object} {{cookiecutter.app_name}} Base angular application object
 */
export default function({{cookiecutter.app_name}}) {
	{{cookiecutter.app_name}}.controller("NavCtrl", ["$scope", "$mdSidenav", "$localStorage", "$location", "$interval",
		function($scope, $mdSidenav, $localStorage, $location, $interval) {
			$scope.nav = {};
			$scope.nav.userData = $localStorage.jwtData;

			$scope.$on("$locationChangeStart", function(event) {
				if ($location.path() == "/login") {
					$scope.nav.show_login_button = false;
				} else {
					$scope.nav.show_login_button = true;
				}
			});

			$scope.go = function(route) {
				$location.path(route);
				// if (route == '/teams/') {
					// CacaoBackend.one('users', $scope.nav.userData.user_id).get().then(function(data) {
						// $location.path(route + data.group[0].id);
					// });
				// }
				// else if (route == '/users/') {
					// $location.path(route + $scope.nav.userData.user_id);
				// }
				// else { $location.path(route); }
			};

			// $scope.get_notifications = function() {
				// NotificationBackend.all('inbox').getList().then(function(data) {
					// if (data.plain().length > 0) {
						// $scope.nav.notifications = data;
					// } else {
						// $scope.nav.notifications = null;
					// }
				// });
			// };

			// $scope.get_notifications_wrapper = function() {
				// $scope.get_notifications();
				// $interval($scope.get_notifications, 30000);
			// };
		}]);
}
