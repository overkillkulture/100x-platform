// 🔐 ARAYA AUTHENTICATION HELPER
// Bridges current login system with secured Araya API

(function() {
    window.ArayaAuth = {
        // Get auth credentials for Araya API calls
        getCredentials: function() {
            // Check if user is logged in
            const userId = localStorage.getItem('workspace_user_id');
            const userName = localStorage.getItem('workspace_user_name');

            if (!userId) {
                return { authenticated: false, error: "Not logged in" };
            }

            // Map known usernames to beta database IDs
            const userMapping = {
                'joshua': { id: '1001', pin: '1001' },
                'Joshua Serrano': { id: '1001', pin: '1001' },
                'toby': { id: '1002', pin: '1002' },
                'Toby Burrowes': { id: '1002', pin: '1002' },
                'wd': { id: '1003', pin: '1003' },
                'WD Brotherton': { id: '1003', pin: '1003' },
                'dean': { id: '1004', pin: '1004' },
                'Dean Sabr': { id: '1004', pin: '1004' },
                'bill': { id: '1005', pin: '1005' },
                'Bill Varni': { id: '1005', pin: '1005' },
                'rutherford': { id: '1006', pin: '1006' },
                'Rutherford': { id: '1006', pin: '1006' }
            };

            // Try to find user in mapping (case-insensitive)
            const userKey = Object.keys(userMapping).find(key =>
                key.toLowerCase() === userId.toLowerCase() ||
                key.toLowerCase() === userName.toLowerCase()
            );

            if (userKey) {
                return {
                    authenticated: true,
                    user_id: userMapping[userKey].id,
                    pin: userMapping[userKey].pin,
                    name: userName
                };
            }

            // If not in mapping, they're not a beta tester yet
            return {
                authenticated: false,
                error: "Not a beta tester",
                message: "You need to be approved as a beta tester to use Araya. Contact the Commander."
            };
        },

        // Check if current user can access Araya
        canAccessAraya: function() {
            const creds = this.getCredentials();
            return creds.authenticated === true;
        },

        // Show login prompt if not authenticated
        requireAuth: function() {
            if (!this.canAccessAraya()) {
                const creds = this.getCredentials();
                alert(creds.message || creds.error || "Please sign in to use Araya");
                window.location.href = '/login';
                return false;
            }
            return true;
        }
    };

    console.log('🔐 Araya Auth Helper loaded');
})();
