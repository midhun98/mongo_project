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
            {data: 'logo'},
            {
                data: null,
                render: function (data) {
                    return '<a href="#" class="btn btn-danger btn-sm delete-career"  data-id="' + data._id + '">Delete</a>';
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
