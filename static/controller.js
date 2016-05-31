

// defines the scope for the main controller for the angular app
angularApp.controller('MainController', ['$scope', '$http', 
    function($scope, $http) {

    // $http.post returns an Object with an attribute named 'data'
    $http.post('/getReminders.json').then(addReminder); 
    
    function addReminder(data) {
        $scope.reminders = [];
        for (var key in data.data) {
            var obj = data.data[key];
            $scope.reminders.push(obj);
        };
        return $scope.reminders;
    }

    $scope.populateModal = function(first, last, phone) {
        $scope.information = {}
        $scope.information['name'] = first + ' ' + last;
        $scope.information[phone] = phone;
        console.log($scope.information);
        return $scope.information;
    }


}]);

