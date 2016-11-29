/**
 * Services provided to the {{cookiecutter.app_name}} application object
 * @param {object} {{cookiecutter.app_name}} Base angular application object
 */
export default function({{cookiecutter.app_name}}) {
	{{cookiecutter.app_name}}.service("$mdLoginToast", ['$mdToast',
		function($mdToast) {
			return {
				show: function(content) {
					return $mdToast.show(
						$mdToast.simple()
							.content(content)
							.position("top right")
							.hideDelay(2000)
					);
				},
			};
		}
	]);
}
