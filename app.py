from flask import Flask, render_template, redirect, url_for, request
from beets.library import Library
import python.beetsCommands as beetsCommands
import python.gitAnnexLib as gitAnnexLib
import python.dictionary as dictionary
import os
from formencode import variabledecode



app = Flask(__name__)


@app.route("/")
def main():
    return redirect(url_for('albumy'))


@app.route('/details')
def details():
    albums_id = request.args.getlist('id',type=int)
    albums = []
    for album_id in albums_id:
        albums.append(lib.get_album(album_id))
    details = beetsCommands.pack_albums_items(albums)

    return render_template('expandeddetails.html', details=details, dictionary=dict)


@app.route('/edit-data', methods = ['GET', 'POST'])
def edit_data():
    if request.method == 'POST':

        postvars = variabledecode.variable_decode(request.form, dict_char='_')

        albums_id = []
        items_id = []
        albums_newdata = []
        items_newdata = []
        items_id_grouped = []       #used to help count number of items
        album_keys_number = len(dict.album_keys)
        item_keys_number = len(dict.item_keys)

        while (len(albums_id)*album_keys_number+len(items_id_grouped)*item_keys_number) != len(postvars):
            albums_number = len(albums_id)

            album_keys_number = len(dict.album_keys)
            item_keys_number = len(dict.item_keys)
            current_len = albums_number * album_keys_number + len(items_id_grouped) * item_keys_number
            album_newdata = []
            for k in range(0, album_keys_number):
                album_newdata.append(postvars.get(str(current_len + k)))
            albums_newdata.append(album_newdata)
            albums_id.append(int(album_newdata[-1]))
            album = lib.get_album(albums_id[-1])

            album_items_id = []
            for item in album.items():
                album_items_id.append(item.id)
                items_id_grouped.append(item.id)
            items_id.append(album_items_id)

            album_items_newdata = []
            for k in range(0, len(album_items_id)):
                item_newdata = []
                for j in range(0, item_keys_number):

                    item_newdata.append(postvars.get(str(albums_number * album_keys_number + (len(items_id_grouped)-len(album_items_id)) * item_keys_number + album_keys_number + k * item_keys_number + j)))
                album_items_newdata.append(item_newdata)
            items_newdata.append(album_items_newdata)

        albums = []
        items = []
        for a, album_id in enumerate(albums_id):
            albums.append(lib.get_album(album_id))              #getting single album
            for k, album_key in enumerate(dict.album_keys):
                if album_key == 'id' or album_key == 'artpath':
                    pass
                elif album_key == 'year':
                    if int(albums_newdata[a][k]) < 10000:
                        albums[a][album_key] = int(albums_newdata[a][k])
                    else:
                        pass
                else:
                    albums[a][album_key] = str(albums_newdata[a][k])


            for i, item_id in enumerate(items_id[a]):
                item = lib.get_item(item_id)
                items.append(item)
                for k, item_key in enumerate(dict.item_keys):
                    if item_key == 'id' or item_key == 'path':
                        pass
                    elif item_key == 'album_id':
                        if int(items_newdata[a][i][k]) in albums_id:
                            item[item_key] = int(items_newdata[a][i][k])
                        else:
                            pass
                    elif item_key == 'disc' or item_key == 'track':
                        if int(items_newdata[a][i][k]) < 100:
                            item[item_key] = int(items_newdata[a][i][k])
                        else:
                            pass
                    else:
                        item[item_key] = str(items_newdata[a][i][k])
                        item['comments'] = 'edited'
                item.try_sync(write=1, move=0)

            albums[a].try_sync(write=True,move=False)
        # for album in albums:
        #     album.load()

        details = beetsCommands.pack_albums_items(albums)

        return render_template('expandeddetails.html', details=details, dictionary=dict)

@app.route("/import")
def get_import_path():
    return render_template('import.html')


@app.route('/startImporting', methods=['POST'])
def startImporting():
    if request.method == 'POST':
        path = request.form['Path']
        albums_id = beetsCommands.beetImport(path)
        for album_id in albums_id:
            album = lib.get_album(album_id)
            for item in album.items():
                item.comments = 'unedited'
                item.write()
            album.store()
            album.load()


        beetsCommands.get_covers(lib)
        return redirect('/albums')


@app.route('/newrepository')
def new_repository():
    return render_template('newrepository.html')


@app.route('/createrepository', methods=['POST'])
def add_remote():
    if request.method == 'POST':
        warning = []
        path = request.form['Path']
        name = request.form['Name']
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            warning.append('Ścieżka musi wskazywać na istniejący folder')
        local_repo.annex_init()
        if name in local_repo.remotes:
            warning.append('Repozytorium o podanej nazwie już istnieje')
        remote_repo = gitAnnexLib.repo(path)
        print(local_repo.connect_remotes(remote_repo, name, 'YAMO_local'))
        local_repo.annex_add()
        local_repo.annex_sync(name)
        print(local_repo.remotes)

        if warning != []:
            return render_template('newrepository.html', warning=warning)
        return redirect('/albums')



@app.route("/albums")
def albumy():
    albums = lib.albums()
    for album in albums:
        album.load()
    alb_sort_album = beetsCommands.pack_albums_items(sorted(albums, key=lambda x: x.album))
    alb_sort_artist = beetsCommands.pack_albums_items(sorted(albums, key=lambda x: x.albumartist))
    alb_sort_year = beetsCommands.pack_albums_items(sorted(albums, key=lambda x: x.year))


    return render_template('albums.html',albums=alb_sort_album, artists=alb_sort_artist, years=alb_sort_year)

@app.route("/artists")
def artysci():
    return render_template('artists.html')

@app.route("/songs")
def muzyka():
    return render_template('songs.html')




if __name__ == "__main__":

    print(beetsCommands.get_library())
    local_repo = gitAnnexLib.repo(beetsCommands.get_library())
    lib = Library(beetsCommands.get_database())
    beetsCommands.get_covers(lib)
    dict = dictionary.dictionary(dictionary.english)

    app.run(debug=True, use_reloader=True)
