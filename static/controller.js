

// defines the scope for the main controller for the angular app
angularApp.controller('MainController', ['$scope', '$interval', function($scope, $interval) {

    $scope.stuff = "Hello, this is working!";

// Calculates reminders every 10 miliseconds and displays on dashboard
    $interval(getReminders, 1000);

    function getReminders() {
        $.post('/getReminders.json', addReminder);
    }
    
    function addReminder(data) {
        $scope.reminders = [];
        for (var key in data) {
            var obj = data[key];
            $scope.reminders.push(obj);
        }
        return $scope.reminders;
    }



}]);
