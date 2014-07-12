'use strict';

/* Controllers */

var playsafeControllers = angular.module('playsafeControllers', []);
 

playsafeControllers.controller('JobListCtrl', function($scope, $http) {
    loadData();

    function loadData() {
        $http.get('../../jobs').success(function(data) {
            $scope.jobs = data;
        });
    };
    
    $scope.refresh = function() {
        loadData();
    };

});

playsafeControllers.controller('JobDetailCtrl', 
        function($scope, $http, $routeParams) {
            $http.get('../../jobs/' + $routeParams.jobId)
              .success(function(data) {
                $scope.job = data;
            });

            $scope.stop = function() {
                $http.post('../../jobs/' + $routeParams.jobId + '/stop')
            };
});

// Controller for handling new urls from job form
playsafeControllers.controller('NewUrlCtrl', function($scope, $http) {
    $scope.submit = function() {
        $http.put('../../jobs', $scope.newurl)
          .success(function() {
              // refresh
              $scope.newurl = '';
              $scope.refresh();
          })
          .error(function(error) {
              console.log(error);
          });
    };
});

