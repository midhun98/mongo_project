/* jshint esversion: 6 */
/*global moment*/
/*global console*/
/*global DataTable*/
/*global swal*/
/*global $*/
/*global csrftoken*/

const brandsData = $.ajax({
    url: "/api/brands/",
});

brandsData.done(function (data) {
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
            {data: 'marketplace'},
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

        // Make an API call to retrieve the marketplace details
        $.ajax({
            url: "/api/brands/" + marketId + "/",
            method: "GET",
            success: function (marketplaceData) {
                // Store the original image URL in a variable
                let originalLogo = marketplaceData.logo;

                // Show the Sweet Alert input fields for editing the marketplace details
                swal.fire({
                    title: 'Edit Marketplace',
                    html: `
                    <input id="name" class="swal2-input" placeholder="Name" value="${marketplaceData.name}">
                    <input id="logo" type="file" class="swal2-input" accept="image/*">
                    <img id="logo-preview" src="${marketplaceData.logo}" alt="Logo Preview" height="50" width="50">`,
                    // Add the necessary buttons and functionality for updating the data
                    showCancelButton: true,
                    confirmButtonText: 'Save Changes',
                    preConfirm: () => {
                        // Retrieve the edited values from the input fields
                        const editedName = document.getElementById('name').value;
                        const editedLogo = document.getElementById('logo').files[0]; // Get the file object

                        // Create a FormData object to send the data to the server (includes the updated logo, if any)
                        const formData = new FormData();
                        formData.append('name', editedName);
                        if (editedLogo) {
                            formData.append('logo', editedLogo);
                        }

                        // Perform the API call to update the marketplace data using the PUT or PATCH method
                        $.ajax({
                            url: "/api/brands/" + marketId + "/",
                            method: "PATCH", // Use PUT or PATCH based on your API's requirements
                            data: formData,
                            processData: false,
                            contentType: false,
                            success: function () {
                                // Handle the successful update here (e.g., show a success message)
                                swal.fire('Changes Saved!', '', 'success');
                            },
                            error: function (error) {
                                // Handle the error here (e.g., show an error message)
                                console.error("Error updating marketplace:", error);
                                swal.fire('Error', 'Error updating the marketplace', 'error');
                            }
                        });
                    }
                });

                // Add an event listener to the file input to handle logo preview
                document.getElementById('logo').addEventListener('change', function (event) {
                    const logoPreview = document.getElementById('logo-preview');
                    const file = event.target.files[0];

                    // Check if a file is selected
                    if (file) {
                        // Create a FileReader to read the file and display a preview
                        const reader = new FileReader();

                        // Define the function to be executed when the FileReader finishes loading
                        reader.onload = function () {
                            logoPreview.src = reader.result;
                        };

                        // Read the file as a URL (data URL)
                        reader.readAsDataURL(file);
                    } else {
                        // If no file is selected or the selection is cancelled, reset the preview
                        logoPreview.src = originalLogo;
                    }
                });
            },
            error: function (error) {
                console.error("Error fetching marketplace details:", error);
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
                    url: "/api/brands/" + marketId + "/",
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
