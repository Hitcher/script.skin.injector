import xbmc
import xbmcvfs
import sys
import html

def create_xsp():
    # 1. Force hide list while writing
    xbmc.executebuiltin('ClearProperty(FilterReady,home)')
    
    # 2. Paths - Moved to special://temp/
    playlist_path = 'special://temp/dynamic_filter.xsp'

    media_type = sys.argv[1] if len(sys.argv) > 1 else "episode"
    xsp_type = "musicvideos" if media_type == "musicvideo" else "movies" if media_type == "movie" else "episodes"
    
    rules = []
    
    # --- Filter Logic ---
    if media_type == "movie":
        title = sys.argv[2] if len(sys.argv) > 2 else ""
        year = sys.argv[3] if len(sys.argv) > 3 else ""
        if title: rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')
        if year:  rules.append(f'<rule field="year" operator="is"><value>{year}</value></rule>')

    elif media_type == "musicvideo":
        artist = sys.argv[2] if len(sys.argv) > 2 else ""
        title = sys.argv[3] if len(sys.argv) > 3 else ""
        if artist: rules.append(f'<rule field="artist" operator="is"><value>{html.escape(artist)}</value></rule>')
        if title:  rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')

    else: # Episode
        show = sys.argv[2] if len(sys.argv) > 2 else ""
        season = sys.argv[3] if len(sys.argv) > 3 else ""
        title = sys.argv[4] if len(sys.argv) > 4 else ""
        if show:   rules.append(f'<rule field="tvshow" operator="is"><value>{html.escape(show)}</value></rule>')
        if season: rules.append(f'<rule field="season" operator="is"><value>{season}</value></rule>')
        if title:  rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')

    # 3. Assemble XML
    rules_string = "\n    ".join(rules)
    xsp_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<smartplaylist type="{xsp_type}">
    <name>Dynamic Filter</name>
    <match>all</match>
    {rules_string}
</smartplaylist>"""

    # 4. Write to temp folder
    f = xbmcvfs.File(playlist_path, 'w')
    f.write(xsp_content)
    f.close()

    # 5. Refresh UI
    xbmc.sleep(100)
    xbmc.executebuiltin('SetProperty(FilterReady,true,home)')
    xbmc.executebuiltin('Container.Refresh')

if __name__ == '__main__':
    create_xsp()
