$(document).ready(function() {
    const table = $('#userTable').DataTable();
    function populateTable(users) {
        table.clear().draw(); // Clear the table

        users.forEach(user => {
            const rowData = [
                user.name,
                user.email,
                user.role,
                '<button id="editUser" class="editUser purplebutton">Edit</button>',
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
    }

    function closeUserModal() {
        $('#userName').val('');
        $('#userEmail').val('');
        $('#userRole').prop('selectedIndex', 0);
        $('#userModal').modal('hide');
    }

    $('#addUser').on('click', function() {
        $('#userName').val('');
        $('#userEmail').val('');

        populateRolesDropdown();
        openUserModal('Add User', 'Add');
    });

    $('#userTable').on('click', '.editUser', function() {
        console.log("Edir click")
        const $row = $(this).closest('tr');
        const name = $row.find('td:eq(0)').text();
        const email = $row.find('td:eq(1)').text();
        const role = $row.find('td:eq(2)').text();
        populateRolesDropdown(role);

        // Populate the modal with user details
        $('#userName').val(name);
        $('#userEmail').val(email);

        openUserModal('Edit User', 'Update');
    });


    $('#saveUser').on('click', function(event) {
        event.preventDefault();

        const name = $('#userName').val();
        const email = $('#userEmail').val();
        const role = $('#userRole option:selected').text();

        const selectedRow = table.row('.selected');
        const dataIndex = selectedRow.index();

        users[dataIndex].name = name;
        users[dataIndex].email = email;
        users[dataIndex].role = role;

        console.log(users);
        const userData = {
            name: name,
            email: email,
            role: role
        };

        let method, url;
        const modalHeading = $('#userModalLabel').text();
        if (modalHeading === 'Add User') {
            method = 'POST';
            url = '/admin/users';
        } else if (modalHeading === 'Edit User') {
            method = 'PUT';
            const userID = table.row('.selected').data()[4];
            url = `/admin/users/${userID}`;
        }

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
            .then(response => {
                if (response.ok) {
                    console.log(`${modalHeading} successful`);
                    populateTable(users);
                } else {
                    console.error(`${modalHeading} failed`);
                }
                closeUserModal();
            })
            .catch(error => {
                console.error('Error:', error);
                closeUserModal();
            });

        closeUserModal();
    });
});
