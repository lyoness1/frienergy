

// defines the scope for the main controller for the angular app
angularApp.controller('MainController', ['$scope', '$http', '$timeout', 
    function($scope, $http, $timeout) {

    // $http.post returns and Object with an attribute named 'data'
    $http.post('/getReminders.json').then(addReminder); 
    
    function addReminder(data) {
        $scope.reminders = [];
        for (var key in data.data) {
            var obj = data.data[key];
            $scope.reminders.push(obj);
        };
        return $scope.reminders;
    }

}]);

