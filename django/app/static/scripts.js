document.addEventListener('DOMContentLoaded', function() {
    // 1. Table Row Linking
    document.addEventListener('click', function (e) {
        const row = e.target.closest('tr.table-row-link[data-href]');
        if (!row || e.target.closest('a, button, input, select, textarea')) return;
        window.location.href = row.getAttribute('data-href');
    });
    document.addEventListener('keydown', function (e) {
        if (e.key !== 'Enter' && e.key !== ' ') return;
        const row = e.target.closest('tr.table-row-link[data-href]');
        if (!row || e.target.closest('a, button')) return;
        e.preventDefault();
        window.location.href = row.getAttribute('data-href');
    });

    // 2. Multiple Select Dropdown Fix
    document.addEventListener('mousedown', function(e) {
        if (e.target.tagName === 'OPTION' && e.target.parentElement.hasAttribute('multiple')) {
            e.preventDefault();
            const select = e.target.parentElement;
            const scroll = select.scrollTop;
            e.target.selected = !e.target.selected;
            select.dispatchEvent(new Event('change', { bubbles: true }));
            select.focus();
            setTimeout(() => { select.scrollTop = scroll; }, 0);
        }
    });

    // 3. Global Table Searching / Filtering
    const tables = document.querySelectorAll('.table-responsive table.table');
    tables.forEach((table) => {
        // Create Search Wrapper
        const searchWrapper = document.createElement('div');
        searchWrapper.className = 'p-3 border-bottom bg-white d-flex justify-content-end align-items-center rounded-top';
        
        // Search Container
        const inputContainer = document.createElement('div');
        inputContainer.className = 'd-flex align-items-center bg-light border rounded-pill px-3 py-2';
        inputContainer.style.maxWidth = '350px';
        inputContainer.style.width = '100%';
        inputContainer.style.transition = 'all 0.2s ease';
        
        inputContainer.addEventListener('focusin', () => {
            inputContainer.classList.remove('bg-light');
            inputContainer.classList.add('bg-white', 'shadow-sm', 'border-success');
        });
        inputContainer.addEventListener('focusout', () => {
            inputContainer.classList.add('bg-light');
            inputContainer.classList.remove('bg-white', 'shadow-sm', 'border-success');
        });

        const searchIcon = document.createElement('i');
        searchIcon.className = 'bi bi-search text-muted me-2';

        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'form-control border-0 bg-transparent shadow-none p-0';
        searchInput.placeholder = 'Search records...';

        inputContainer.appendChild(searchIcon);
        inputContainer.appendChild(searchInput);
        searchWrapper.appendChild(inputContainer);

        // Insert before the table-responsive div (which is inside the card-body)
        const tableResponsive = table.parentElement;
        tableResponsive.parentNode.insertBefore(searchWrapper, tableResponsive);

        // Filter Logic
        searchInput.addEventListener('keyup', function(e) {
            const term = e.target.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            let visibleCount = 0;
            rows.forEach((row) => {
                // Ignore the empty state row if it exists
                if (row.querySelector('td[colspan]')) return;
                
                const text = row.textContent.toLowerCase();
                if (text.includes(term)) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
});
