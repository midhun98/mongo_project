/* jshint esversion: 6 */
/*global moment*/
/*global console*/
/*global DataTable*/
/*global swal*/
/*global $*/
/*global csrftoken*/

const careerData = $.ajax({
    url: "/api/users/",
});

careerData.done(function (data) {
    'use strict';

    // Initialize the datatable
    $('#careers-table').DataTable({
        data: data,
        columns: [
            {data: 'name'},
            {data: 'email'},
        ]
    });
});
