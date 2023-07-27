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
                    let editButton = '<a href="#" class="btn btn-primary btn-sm edit-career" data-id="' + data._id + '">Edit</a>';
                    let deleteButton = '<a href="#" class="btn btn-danger btn-sm delete-career" data-id="' + data._id + '">Delete</a>';
                    return editButton + ' ' + deleteButton;
                }
            }
        ]
    });

    $(document).on("click", ".edit-career", function () {
        let marketId = $(this).data("id");
        let row = $(this).closest("tr");

        // You can fetch the existing data for the marketplace using an API call here, if needed.
        // For simplicity, let's assume the data is already available in a variable called 'marketplaceData'.

        // Show the Sweet Alert input fields for editing the marketplace details
        swal.fire({
            title: 'Edit Marketplace',
            html: `
            <input id="name" class="swal2-input" placeholder="Name" value="">
            <input id="logo" class="swal2-input" placeholder="Logo URL" value="">
        `,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Save Changes',
            preConfirm: () => {
                const name = swal.getPopup().querySelector('#name').value;
                const logo = swal.getPopup().querySelector('#logo').value;
                return {name: name, logo: logo};
            }
        }).then((result) => {
            if (!result.dismiss) {
                const editedData = result.value;
                // Make a PATCH request to update the marketplace details
                $.ajax({
                    type: "PATCH",
                    url: "/api/marketplaces/" + marketId + "/",
                    headers: {
                        'Content-type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    data: JSON.stringify(editedData),
                    success: function () {
                        // Update the data in the table (if needed)
                        // For simplicity, let's assume we don't need to update the table data here.
                        swal.fire(
                            'Saved!',
                            'Changes have been saved.',
                            'success'
                        );
                    },
                    error: function () {
                        swal.fire(
                            'Error!',
                            'An error occurred while saving changes.',
                            'error'
                        );
                    }
                });
            }
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
