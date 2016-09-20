(function () {
    var app = angular.module("mainPageApp", ["xeditable"])  // "ngResource", "ngCookie",
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    });

    app.run(function (editableOptions) {
        editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
    });

    app.controller("ProfileController", function () {

    });

    app.controller("PartonController", function () {

    });

    // FOTO GALLERY
    app.controller("FotoCtrl", function($scope, $http) {
        $scope.albums;
        $scope.current_album_name = [];
        $scope.foto = {};

        $http.get("/api/v1/album/")
            .then(function successCallback(response) {                            
                $scope.albums = response.data.objects;
                console.log($scope.albums);
                // заместо init , сначала находим id последнего фестиваля                
                $scope.last_album_id = $scope.albums[0].id;
                $scope.getFoto($scope.last_album_id);
            },
            function errorCallback(response) {
                console.log("error in angular foto " + response);
            });

        // get fotos from album
        $scope.getFoto = function(album_id) {
            console.log("--inside album_id get--");
            console.log(album_id);

            // find album_title by id            
            $scope.current_album_name = jQuery.grep($scope.albums, function (obj) {                
                return obj.id === album_id;
            })[0].title;
            
            $http.get("/api/v1/foto/?album_id__id=" + album_id)
                .then(function successCallback(response) {                    
                    $scope.foto = response.data.objects;
                    console.log($scope.foto);
                },
                function errorCallback(response) {
                    console.log("error in get foto from album " );
                    console.log(response);
                });
        };       
    });

})();