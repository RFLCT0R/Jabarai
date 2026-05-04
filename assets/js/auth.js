// Supabase Auth Helper - Include this on all pages that need auth state

// Initialize Supabase (make sure config.js is loaded before this)
let supabaseClient = null;

function initSupabase() {
    if (typeof SUPABASE_CONFIG !== 'undefined' && !supabaseClient) {
        supabaseClient = window.supabase.createClient(
            SUPABASE_CONFIG.url,
            SUPABASE_CONFIG.anonKey
        );
    }
    return supabaseClient;
}

// Get current session
async function getSession() {
    const supabase = initSupabase();
    if (!supabase) return null;
    
    const { data: { session } } = await supabase.auth.getSession();
    return session;
}

// Get current user
async function getUser() {
    const supabase = initSupabase();
    if (!supabase) return null;
    
    const { data: { user } } = await supabase.auth.getUser();
    return user;
}

// Sign out
async function signOut() {
    const supabase = initSupabase();
    if (!supabase) return;
    
    await supabase.auth.signOut();
    localStorage.removeItem('supabase_session');
}

// Track current auth state to prevent unnecessary re-renders
let currentAuthState = null;
let currentUserId = null;

// Update UI based on auth state
async function updateAuthUI() {
    const session = await getSession();
    const navActions = document.querySelector('.nav-actions');
    
    if (!navActions) return;

    // Determine new state
    const newState = session ? 'logged_in' : 'logged_out';
    const newUserId = session?.user?.id || null;
    
    // Only update if state actually changed
    if (currentAuthState === newState && currentUserId === newUserId) {
        return; // No change, skip re-render
    }
    
    // Update tracked state
    currentAuthState = newState;
    currentUserId = newUserId;

    if (session) {
        // User is logged in - show icon + family name
        const user = session.user;
        const fullName = user.user_metadata?.full_name || user.email?.split('@')[0] || 'User';
        const familyName = fullName.split(' ')[0] || fullName;
        const email = user.email || '';
        
        // Get avatar from Google OAuth or use initial placeholder
        const avatarUrl = user.user_metadata?.avatar_url || user.user_metadata?.picture || null;
        const initial = familyName.charAt(0).toUpperCase();
        const avatarHtml = avatarUrl 
            ? `<img src="${avatarUrl}" alt="${familyName}" class="user-avatar" onerror="this.outerHTML='<span class=\'user-initial\'>${initial}</span>'">`
            : `<span class="user-initial">${initial}</span>`;

        navActions.innerHTML = `
            <div class="user-menu">
                <a href="user_page.html" class="user-trigger">
                    <div class="user-icon-wrapper">
                        ${avatarHtml}
                    </div>
                    <span class="user-family-name">${familyName}</span>
                </a>
                <div class="user-dropdown">
                    <div class="user-profile">
                        <div class="user-profile-name">${fullName}</div>
                        <div class="user-profile-email">${email}</div>
                    </div>
                    <div class="user-dropdown-divider"></div>
                    <a href="user_page.html" class="dropdown-link">
                        <i class="fas fa-user"></i> My Account
                    </a>
                    <a href="#" onclick="signOut(); return false;" class="logout-link">
                        <i class="fas fa-sign-out-alt"></i> Log out
                    </a>
                </div>
            </div>
        `;
    } else {
        // User is not logged in - show Get Started button
        navActions.innerHTML = `
            <a href="register.html" class="btn-signup">Get Started</a>
        `;
    }
}

// Auto-initialize auth UI on page load
document.addEventListener('DOMContentLoaded', () => {
    // Only update UI if Supabase is configured
    if (typeof SUPABASE_CONFIG !== 'undefined' && SUPABASE_CONFIG.url !== 'YOUR_SUPABASE_PROJECT_URL') {
        updateAuthUI();
    }
});

// Listen for auth state changes
if (typeof SUPABASE_CONFIG !== 'undefined' && SUPABASE_CONFIG.url !== 'YOUR_SUPABASE_PROJECT_URL') {
    const supabase = initSupabase();
    if (supabase) {
        supabase.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_OUT') {
                localStorage.removeItem('supabase_session');
            } else if (event === 'SIGNED_IN' && session) {
                localStorage.setItem('supabase_session', JSON.stringify(session));
            }
            updateAuthUI();
        });
    }
}
