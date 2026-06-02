document.addEventListener('alpine:init', () => {
    // ── Dedicated Reader preferences store ──
    Alpine.store('reader', {
        theme: localStorage.getItem('novella_reader_theme') || 'parchment',
        fontSize: localStorage.getItem('novella_reader_size') || 'lg', // 'md' | 'lg' | 'xl' | '2xl'
        fontFamily: localStorage.getItem('novella_reader_font') || 'serif', // 'serif' | 'sans'
        lineHeight: localStorage.getItem('novella_reader_height') || 'relaxed', // 'normal' | 'relaxed' | 'loose'
        progress: JSON.parse(localStorage.getItem('novella_reader_progress')) || {},
        bookmarks: JSON.parse(localStorage.getItem('novella_reader_bookmarks')) || [],

        init() {
            this.applyTheme();
        },

        setTheme(newTheme) {
            this.theme = newTheme;
            localStorage.setItem('novella_reader_theme', newTheme);
            this.applyTheme();
        },

        applyTheme() {
            document.documentElement.setAttribute('data-reading-theme', this.theme);
        },

        setFontSize(size) {
            this.fontSize = size;
            localStorage.setItem('novella_reader_size', size);
        },

        setFontFamily(family) {
            this.fontFamily = family;
            localStorage.setItem('novella_reader_font', family);
        },

        setLineHeight(height) {
            this.lineHeight = height;
            localStorage.setItem('novella_reader_height', height);
        },

        // Save progress (e.g. scroll state)
        saveProgress(chapterId, percentage) {
            this.progress[chapterId] = percentage;
            localStorage.setItem('novella_reader_progress', JSON.stringify(this.progress));
        },

        getProgress(chapterId) {
            return this.progress[chapterId] || 0;
        },

        // Bookmark chapter
        toggleBookmark(chapterId, title, lineHash) {
            const index = this.bookmarks.findIndex(b => b.chapterId === chapterId && b.lineHash === lineHash);
            if (index > -1) {
                this.bookmarks.splice(index, 1);
            } else {
                this.bookmarks.push({
                    id: Math.random().toString(36).substr(2, 9),
                    chapterId,
                    title,
                    lineHash,
                    createdAt: new Date().toISOString()
                });
            }
            localStorage.setItem('novella_reader_bookmarks', JSON.stringify(this.bookmarks));
        },

        isBookmarked(chapterId, lineHash) {
            return this.bookmarks.some(b => b.chapterId === chapterId && b.lineHash === lineHash);
        }
    });
});
