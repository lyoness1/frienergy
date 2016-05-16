
// defines the angular app
var angularApp = angular.module('frienergyApp', []);

// configures angular brackets for integration with jinja
angularApp.config(['$interpolateProvider', function($interpolateProvider) {

    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');

}]);