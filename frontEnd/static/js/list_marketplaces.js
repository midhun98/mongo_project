/* jshint esversion: 6 */
/*global moment*/
/*global console*/
/*global DataTable*/
/*global swal*/
/*global $*/
/*global csrftoken*/

const careerData = $.ajax({
    url: "/api/marketplaces/",
});

careerData.done(function (data) {
    'use strict';

    // Initialize the datatable
    $('#careers-table').DataTable({
        data: data,
        columns: [
            {data: 'name'},
            {
                data: 'logo',
                render: function (data) {
                    if (data) {
                        // If the logo exists, show it as an image
                        return '<img src="' + data + '" alt="Logo" height="50" width="50">';
                    } else {
                        // If the logo doesn't exist, show a placeholder or an empty image
                        return '<img src="" alt="No Logo" height="50" width="50">';
                    }
                }
            },
            {
                data: null,
                render: function (data) {
                    var editButton = '<a href="#" class="btn btn-primary btn-sm edit-career" data-id="' + data._id + '">Edit</a>';
                    var deleteButton = '<a href="#" class="btn btn-danger btn-sm delete-career" data-id="' + data._id + '">Delete</a>';
                    return editButton + ' ' + deleteButton;
                }
            }
        ]
    });

    $(document).on("click", ".view-message-btn", function () {
        let message = $(this).attr("data-message");
        swal.fire({
            title: 'Message',
            text: message,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'OK'
        });
    });

    $(document).on("click", ".delete-career", function () {
        let marketId = $(this).data("id");
        let row = $(this).closest("tr");
        swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    type: "DELETE",
                    url: "/api/marketplaces/" + marketId + "/",
                    headers: {
                        'Content-type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    success: function () {
                        swal.fire(
                            'Deleted!',
                            'Item deleted.',
                            'success'
                        );
                        //removing the row
                        row.remove();
                    },
                    error: function () {
                        swal.fire(
                            'Error!',
                            'An error occurred while deleting the item.',
                            'error'
                        );
                    }
                });
            }
        });
    });
});
