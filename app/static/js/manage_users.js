$(document).ready(function() {
    let dataIndex = null;
    const table = $('#userTable').DataTable();
    function populateTable(users) {
        table.clear().draw(); // Clear the table

        users.forEach((user, index) => {
            const rowData = [
                user.name,
                user.email,
                user.role,
                `<button id="editUser_${index}" class="editUser purplebutton">Edit</button>`,
                user.id
            ];

            table.column(4).visible(false);
            table.row.add(rowData).draw(false);
        });
    }
    populateTable(users);

    $('#userTable tbody').on('click', 'tr', function() {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    function populateRolesDropdown(selectedRole = null) {
        $.ajax({
            url: '/roles',
            type: 'GET',
            success: function(response) {
                const roles = response.data;
                const roleDropdown = $('#userRole');
                roleDropdown.empty();
                roleDropdown.val('');

                roles.forEach((role, index) => {
                    roleDropdown.append($('<option></option>').attr('value', role.id).text(role.name));
                    if (selectedRole && role.name === selectedRole) {
                        roleDropdown.val(role.id);
                    }
                });
            },
            error: function(error) {
                console.error('Error fetching roles:', error);
            }
        });
    }

    function openUserModal(title, buttonText) {
        $('#userModalLabel').text(title);
        $('#saveUser').text(buttonText);
        $('#userModal').modal('show');
        $('#userError').text("").hide();
    }

    function closeUserModal() {
        $('#userName').val('');
        $('#userEmail').val('');
        $('#userRole').prop('selectedIndex', 0);
        $('#userModal').modal('hide');
        $('#userError').text("").hide();
    }

    $('#addUser').on('click', function() {
        $('#userName').val('');
        $('#userEmail').val('');

        populateRolesDropdown();
        openUserModal('Add User', 'Add');
    });

    $('#userTable').on('click', '.editUser', function() {
        console.log("Edit click")
        const $row = $(this).closest('tr');
        const name = $row.find('td:eq(0)').text();
        const email = $row.find('td:eq(1)').text();
        const role = $row.find('td:eq(2)').text();
        populateRolesDropdown(role);

        dataIndex = $(this).attr("id").split("_")[1];

        // Populate the modal with user details
        $('#userName').val(name);
        $('#userEmail').val(email);

        openUserModal('Edit User', 'Update');
    });

    function addUser() {
        const name = $('#userName').val();
        const email = $('#userEmail').val();
        const role = $('#userRole option:selected').text();

        const userData = {
            name: name,
            email: email,
            role: role
        };

        fetch('/admin/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
            .then(response => {
                return response.json()
            })
            .then(responseData => {
                console.log(responseData);
                if ("data" in responseData) {
                    console.log('Add User successful');
                    users.push(responseData.data);
                    populateTable(users);
                    console.log(users);
                    closeUserModal();
                } else {
                    console.log('Error:', responseData);
                    $('#userError').text(responseData.message).show();
                }
            })
            .catch(errorResponse => {
                console.error('Error:', errorResponse);
                errorResponse.json().then(errorData => {
                    $('#userError').text(errorData.message).show();
                }).catch(() => {
                    $('#userError').text('An error occurred. Please try again.').show();
                });
            });
    }

    function editUser() {
        const name = $('#userName').val();
        const email = $('#userEmail').val();
        const role = $('#userRole option:selected').text();

        const userData = {
            name: name,
            email: email,
            role: role
        };

        fetch(`/admin/users/${dataIndex}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
            .then(response => {
                return response.json();
            })
            .then(responseData => {
                if ("data" in responseData) {
                    console.log('Edit User successful');
                    users[dataIndex].name = name;
                    users[dataIndex].email = email;
                    users[dataIndex].role = role;
                    populateTable(users);
                    closeUserModal();
                } else {
                    console.log('Error:', responseData);
                    $('#userError').text(responseData.message).show();
                }
            })
            .catch(errorResponse => {
                console.error('Error:', errorResponse);
                errorResponse.json().then(errorData => {
                    $('#userError').text(errorData.message).show();
                }).catch(() => {
                    $('#userError').text('An error occurred. Please try again.').show();
                });
            });
    }

    $('#saveUser').on('click', function(event) {
        event.preventDefault();

        const modalHeading = $('#userModalLabel').text();

        if (modalHeading === 'Add User') {
            addUser();
        } else if (modalHeading === 'Edit User') {
            editUser();
        }
    });

});
