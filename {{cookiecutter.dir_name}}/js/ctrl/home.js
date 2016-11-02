/**
 * Home Controller
 * @param {object} {{cookiecutter.app_name}} Base angular application object
 */
export default function({{cookiecutter.app_name}}) {
	{{cookiecutter.app_name}}.controller("HomeCtrl", ["$scope", "$location",
		function($scope, $location) {
			$scope.home = [
// LOAD HOMEITEMS
			];
		}]);
}
