import xbmc
import xbmcvfs
import sys
import html
import os

def create_xsp():
    # 1. Force hide list while writing
    xbmc.executebuiltin('ClearProperty(FilterReady,home)')
    
    # 2. Define path inside addon_data as per Repo requirements
    addon_id = "script.skin.injector"
    profile_dir = 'special://profile/addon_data/' + addon_id + '/'
    playlist_path = profile_dir + 'dynamic_filter.xsp'

    # Ensure the addon_data subfolder exists
    if not xbmcvfs.exists(profile_dir):
        xbmcvfs.mkdirs(profile_dir)

    # 3. Capture arguments safely using slice extraction (prevents IndexError)
    media_type_slice = sys.argv[1:2]
    media_type = media_type_slice[0] if media_type_slice else "episode"
    
    # Map the correct smart playlist type string required by Kodi
    if media_type == "musicvideo":
        xsp_type = "musicvideos"
    elif media_type == "movie":
        xsp_type = "movies"
    elif media_type == "tvshow":
        xsp_type = "tvshows"
    else:
        xsp_type = "episodes"
    
    rules = []
    
    if media_type == "movie":
        title_slice = sys.argv[2:3]
        year_slice = sys.argv[3:4]
        title = title_slice[0] if title_slice else ""
        year = year_slice[0] if year_slice else ""
        
        if title: rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')
        if year:  rules.append(f'<rule field="year" operator="is"><value>{year}</value></rule>')

    elif media_type == "tvshow":
        title_slice = sys.argv[2:3]
        year_slice = sys.argv[3:4]
        title = title_slice[0] if title_slice else ""
        year = year_slice[0] if year_slice else ""
        
        if title: rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')
        if year:  rules.append(f'<rule field="year" operator="is"><value>{year}</value></rule>')

    elif media_type == "musicvideo":
        artist_slice = sys.argv[2:3]
        title_slice = sys.argv[3:4]
        artist = artist_slice[0] if artist_slice else ""
        title = title_slice[0] if title_slice else ""
        
        if artist: rules.append(f'<rule field="artist" operator="is"><value>{html.escape(artist)}</value></rule>')
        if title:  rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')

    else: # Episode
        file_path_slice = sys.argv[2:3]
        season_slice = sys.argv[3:4]
        title_slice = sys.argv[4:5]
        
        file_path = file_path_slice[0] if file_path_slice else ""
        season = season_slice[0] if season_slice else ""
        title = title_slice[0] if title_slice else ""
        
        if file_path:
            # Safely acts on a pure string object now
            clean_path = os.path.normpath(file_path.replace('\\', '/'))
            
            # v0.0.2: Extract pure unique filename (e.g. S01E01.mkv)
            pure_filename = os.path.basename(clean_path)
            
            # v0.0.2: Extract the parent show folder name safely (e.g. Dark Matter (2015))
            path_parts = clean_path.split(os.sep)
            if len(path_parts) >= 3 and "Season" in path_parts[-2]:
                show_folder = path_parts[-3]
            elif len(path_parts) >= 2:
                show_folder = path_parts[-2]
            else:
                show_folder = ""

            if pure_filename:
                rules.append(f'<rule field="filename" operator="is"><value>{html.escape(pure_filename)}</value></rule>')
            if show_folder:
                rules.append(f'<rule field="path" operator="contains"><value>{html.escape(show_folder)}</value></rule>')
            
        if season: rules.append(f'<rule field="season" operator="is"><value>{season}</value></rule>')
        if title:  rules.append(f'<rule field="title" operator="is"><value>{html.escape(title)}</value></rule>')

    # 4. Assemble XML
    rules_string = "\n    ".join(rules)
    xsp_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<smartplaylist type="{xsp_type}">
    <name>Dynamic Filter</name>
    <match>all</match>
    {rules_string}
</smartplaylist>"""

    # 5. Write to disk
    f = xbmcvfs.File(playlist_path, 'w')
    f.write(xsp_content)
    f.close()

    # 6. Refresh UI
    xbmc.sleep(250)
    xbmc.executebuiltin('SetProperty(FilterReady,true,home)')
    xbmc.executebuiltin('Container.Refresh')

if __name__ == "__main__":
    create_xsp()
