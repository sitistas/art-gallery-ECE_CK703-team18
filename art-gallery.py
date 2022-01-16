#Εισαγωγή απαραίτητων βιβλιοθηκών
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.messagebox import askyesno
import sqlite3

#Χρωματική Παλέτα
button_color = '#F1FDFF'
bg_color = '#b2ebf2'
light_color = '#e0f7fa'
white = '#ffffff'

#Σύνδεση με την βάση δεδομένων 
con = sqlite3.connect('art-gallery.db')
#Δημιουργία cursor για την εκτέλεση των SQL εντολών
c = con.cursor()
#Ενεργοποίηση ελέγχων ξένων κλειδιών
c.execute('PRAGMA foreign_keys=ON')

#Αφαίρεση όλων των στοιχείων από το Treeview
def clear_treeview():
    for i in tree_view.get_children():
         tree_view.delete(i)

#Εισαγωγή των αποτελεσμάτων ενός query στο Treeview
def tree_view_insert(data):
    for row in data:
        tree_view.insert('', 'end', values=row)

#Προσαρμογή όλων των παραθύρων ώστε να έχουν το ίδιο χρώμα
def add_style(app):
    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure("Treeview", background = light_color)
    style.configure('TButton', background =button_color)
    style.configure('TEntry', background = light_color)
    style.configure('TLabel', background = bg_color)
    style.configure('TCombobox', background = bg_color)
    app.configure(bg=bg_color)

#Γενική Αναζήτηση
def search_by():
    try:
        entity = cbox1.get() #Ανάκτηση οντότητας
        criter = cbox2.get() #Ανάκτηση κριτηρίου αναζήτησης
        term = artist_search_entry.get() #Ανάκτηση εισόδου χρήστη
        query_str="SELECT * FROM "+entity+" WHERE "+criter+" LIKE '%"+str.title(term)+"%'" #Query 
        find(query_str) #Εκτέλεση query και εκτύπωση αποτελεσμάτων
    except: pass  


#Σύνθετη αναζήτηση
def adv_search():
    try:
        entity = cbox1.get() #Ανάκτηση οντότητας
        criter1 = crit1_box.get() #Ανάκτηση 1ου κριτηρίου αναζήτηση
        criter2 = crit2_box.get() #Ανάκτηση 2ου κριτηρίου κ.ο.κ.
        criter3 = crit3_box.get()
        criter4 = crit4_box.get()
        term1 = crit1_search_entry.get() #Ανάκτηση εισόδου για το πρώτο κριτήριο
        term2 = crit2_search_entry.get() #Ανάκτηση για το 2ο κ.ο.κ.
        term3 = crit3_search_entry.get()
        term4 = crit4_search_entry.get()
        temp1=[criter1, criter2, criter3, criter4] #Λίστα με τις τιμές όλων των comboboxes των κριτηρίων
        temp2=[term1, term2, term3, term4] #Λίστα με τις τιμές όλων των σχετικών entries
        critlist=[] #Λίστα με τα κριτήρια που έχουμε επιλέξει
        termlist=[] #Λίστα με τις εισόδους όπου έχουμε δώσει κάποια τιμή
        for i in range(len(temp1)):
            if temp1[i]!='':
                critlist.append(temp1[i])
                termlist.append(temp2[i])
        if termlist==[]: return
        #Εκτέλεση query
        query_str="SELECT * FROM "+entity+" WHERE "+critlist[0]+" LIKE '%"+str.title(termlist[0])+"%'"
        for i in range(1, len(termlist)):
            query_str+=" AND "+critlist[i]+" LIKE '%"+str.title(termlist[i])+"%'"
        find(query_str)
    except: pass

#Εμφάνιση όλων των τιμών της οντότητας που υπάρχει στο search bar
def show_all():
    ont=cbox1.get()  #Ανάκτηση σχετικής οντότητας
    query="SELECT * FROM "+ont
    find(query)

#Κουμπί κλεισίματος     
def close():
    con.close() #Κλείσιμο σύνδεσης με τη βάση
    app.destroy() #Κλείσιμο του παραθύρου

#Τρέξιμο εντολής sql με το κουμπί run
def runsql(txt_edit, query_win):
    query = txt_edit.get("1.0", END) #Ανάκτηση της εισόδου από το πλαίσιο κειμένου και αποθήκευσή της σε str για εκτέλεση του query
    try:
        c.execute(query)
    except: #Σε περίπτωση κλεισίματος του βασικού παραθύρου ενώ είναι ακόμα ανοιχτό το παράθυρο 'Run query', 
        #η σύνδεση με τη βάση χάνεται, οπότε εδώ την επαναφέρουμε
        con = sqlite3.connect('art-gallery.db')
        c = con.cursor()
    try:
        c.execute(query)
        data1 = c.fetchall()
        columns= [description[0] for description in c.description] #Τίτλοι των στηλών των αποτελεσμάτων που πήραμε από το query
        results_win = Tk() #Παράθυρο αποτελεσμάτων
        add_style(results_win)
        results_win.title("Results")
        res_frame=Frame(results_win)
        res_frame.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
        tree_view = ttk.Treeview(res_frame, columns=columns, show="headings") #Treeview για την εκτύπωση των αποτελεσμάτων
        len_count=0 #Counter για την ανάγνωση του πρώτου tuple που επιστρέφει το query για ρύθμιση του πλάτους των στηλών
        for col in columns: #Ρύθμιση του πλάτους των στηλών
            wid=len(str(data1[0][len_count])) #Μήκος της πρώτης τιμής που επιστρέφεται για τη στήλη col
            if wid>4 or wid==0:
                tree_view.column(col, width=200)
            else:
                tree_view.column(col, width=80)
            tree_view.heading(col, text=col)
            len_count+=1
        tree_view.pack(side="left", fill="y")
        scrollbar = Scrollbar(res_frame, orient='vertical') #Δημιουργία scrollbar για το tree
        scrollbar.configure(command=tree_view.yview)
        scrollbar.pack(side="right", fill="y")
        tree_view.config(yscrollcommand=scrollbar.set)
        for row in data1:
            tree_view.insert('', 'end', values=row)
        results_win.mainloop()
    except Exception as ex: 
        messagebox.showerror('Error', str.title(str(ex))) #Errorbox σε περίπτωση εισόδου μη έγκυρου ID
        query_win.lift()

#Άνοιγμα παραθύρου για είσοδο query
def runquery():
    query_win = Tk()
    add_style(query_win)
    query_win.title("Run a query")
    query_win.geometry('650x450')
    txt_edit = Text(query_win) #Πλαίσιο κειμένου
    fr_buttons = Frame(query_win, bg=bg_color) #Frame για τα κουμπιά Run, Quit
    btn_open = ttk.Button(fr_buttons, text="Run", command= lambda: runsql(txt_edit, query_win))
    btn_save = ttk.Button(fr_buttons, text="Quit", command=query_win.destroy)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=0, column=1, sticky="ew", padx=5)
    fr_buttons.grid(row=1, column=0, sticky="ns")
    txt_edit.grid(row=0, column=0, sticky="nsew")

#Ενημέρωση comboboxes όταν αλλάζει το combobox οντότητας
def selected(event):
    insert_btn.config(command=new) #Ενεργοποίηση του κουμπιού 'Insert'
    showall_btn.config(command=show_all) #Ενεργοποίηση του κουμπιού 'Show all'
    attr_list=[]
    ont=cbox1.get() #Ανάκτηση οντότητας από το βασικό combobox
    c.row_factory = lambda cursor, row: row[0] #Παίρνουμε STRs αντί για tuples
    c.execute("SELECT name FROM PRAGMA_table_info('"+ont+"')")
    data=c.fetchall()
    for i in data:
        attr_list.append(i) #Προσθήκη κάθε attribute της επιλεγμένης οντότητας στη λίστα attr_list
    cbox2['values']=attr_list #Η λίστα attr_list γίνεται η λίστα επιλογών του combobox 2 που χρησιμοποιείται για απλή αναζήτηση
    cbox2.current(0) #Το πρώτο attribute τίθεται ως προεπιλεγμένη τιμή
    #Ενημέρωση των επιλογών των comboboxes της σύνθετης αναζήτησης
    crit1_box['values']=attr_list
    crit2_box['values']=attr_list
    crit3_box['values']=attr_list
    crit4_box['values']=attr_list  
    c.row_factory = None #Αναίρεση της προηγούμενης αλλαγής για τα tuples

#Αναζήτηση δανεισμένων έργων
def poa_collector_search():
    query='SELECT Title, Name, Borrow_Date, Return_Date FROM Collector as c JOIN Piece_of_Art as p ON c.ID = p.Owner_ID ORDER BY Return_Date desc'
    find(query)

#Αναζήτηση έργων τέχνης ενός καλλιτέχνη
def pieces_of_artist():
    artist_selection = str.title(pieces_of_artist_entry.get()) #Ανάκτηση εισόδου για τον καλλιτέχνη
    query = "SELECT p.ID as Painting_ID, Title, t.Full_name, c.name as Collection_Name, Year_of_creation, Type, Height, Width, Depth FROM (Artist as a JOIN Piece_of_Art as p ON a.ID = p.Artist_ID) as t JOIN Collection as c ON c.ID = t.Collection_ID  WHERE a.Full_Name LIKE '%" + artist_selection + "%'"
    find(query)

#Συνάρτηση για εύρεση εκθέσεων που επισκέπτονται ανά ξενάγηση
def exh_per_tour():
    group_nameorid = str.title(exh_per_tour_entry.get()) #Ανάκτηση της εισόδου που είναι είτε το ID είτε όνομα του γκρουπ
    query = "SELECT e.Title as Exhibition_Title, g.ID as Group_ID, g.Group_Name, g.Number_of_participants, g.Date_time FROM (Guided_Tour as g JOIN Is_Presented as i ON g.ID = i.GT_ID) as gi JOIN Exhibition as e on gi.EXH_ID = e.ID WHERE g.ID ='"+ group_nameorid+"' OR g.Group_Name LIKE '%"+group_nameorid+"%'"
    find(query)

#Συνάρτηση για εύρεση έργων τέχνης ανά έκθεση
def poa_per_exh():
    exh_nameorid = str.title(poa_per_exh_entry.get()) #Ανάκτηση ονόματος ή ID έκθεσης που έχει εισαχθεί
    query = "SELECT e.Title as Exhibition_Title, p.ID as Painting_ID, p.Title as Piece_of_Art_Title, a.Full_Name as Artist_Name, c.name as Collection_Name, Year_of_creation, Type, Height, Width, Depth FROM (((Exhibition as e JOIN Shown as s ON e.ID = s.EXH_ID) JOIN Piece_of_Art as p on s.AP_ID = p.ID) JOIN Collection as c on c.ID = p.Collection_ID) JOIN Artist as a on a.ID = p.Artist_ID WHERE (e.ID = '"+exh_nameorid+"' OR e.Title LIKE '%"+exh_nameorid+"%') AND End_date > datetime('now')"
    find(query)

#Συνάρτηση για εύρεση των έργων που απουσιάζουν λόγω συντήρησης
def maint_poa():
    query="SELECT Title, Starting_date, Expected_return FROM (Piece_of_Art as p join Under_maint as u on u.AP_ID = p.ID) JOIN Maintenance as m on m.ID = u.Maint_ID WHERE Starting_date < datetime('now') AND Expected_return > datetime('now')"
    find(query)

#Συνάρτηση εύρεσης πλήθους έργων ανά συλλογή
def count_poa_per_collection():
    query="SELECT  c.id, c.name, count(*) as Total_Pieces_Of_Art FROM Piece_of_Art as p join Collection as c on c.id = p.Collection_ID GROUP BY Collection_ID ORDER BY count(*) DESC"
    find(query)

#Συνάρτηση εκτέλεσης query, ανάκτησης και εμφάνισης αποτελεσμάτων
def find(query):
    clear_treeview() #Εκκαθάριση του treeview
    c.execute(query) #Εκτέλεση query
    data1 = c.fetchall() #Ανάκτηση αποτελεσμάτων
    tree_view_insert(data1) #Εισαγωγή αποτελεσμάτων στο treeview
    printcolumns(data1) #Ρύθμιση στηλών του treeview

#Συνάρτηση ρύθμισης των στηλών του treeview
def printcolumns(data1):
    attribs= [description[0] for description in c.description] #Τίτλοι των στηλών των αποτελεσμάτων που επέστρεψε το query
    len_count=0 #Counter για την ανάγνωση του πρώτου tuple που επιστρέφει το query για ρύθμιση του πλάτους των στηλών
    for i in range(0, len(attribs)):
        if i==11: break #11 είναι το πλήθος των στηλών που έχουμε επιλέξει να εμφανίζονται
        tree_view.heading(i, text=attribs[i])
        if len(data1)!=0: 
            wid=len(str(data1[0][len_count])) #Μήκος του πρώτου αποτελέσματος που έχει επιστραφεί ανά στήλη
            if wid>4 or wid==0:
                tree_view.column(i, width=200)
            else:
                tree_view.column(i, width=80)
            len_count+=1
    i+=1
    while i<11: #Εκκαθάριση τίτλου κενών στηλών
        tree_view.heading(i, text='')
        i+=1

#Συνάρτηση διαμόρφωσης του παραθύρου επεξεργασίας για τα κουμπιά edit, insert
def makeform(root, fields, command, sel=[]): #fields είναι οι τίτλοι των attributes, 
    #sel είναι τα attributes του συγκεκριμένου αντικειμένου που επεξεργαζόμαστε
    entries=[]

    if command=='edit': #Παράθυρο επεξεργασίας
        row1 = Frame(root)	
        lab1 = ttk.Label(row1, width=12, text=fields[0]+":", anchor='w')
        lab2 = ttk.Label(row1, width=12, text=sel[0], anchor='w')        
        row1.pack(side=TOP, fill	= X, padx = 5, pady=5)	
        lab1.pack(side=LEFT)	
        lab2.pack(side=RIGHT, expand = YES, fill	= X)
        j=1 #Σε περίπτωση επεξεργασίας, το πρώτο entrybox αντικαθίσταται από label, καθώς για την επεξεργασία έχουμε
            #δεχτεί ότι το πρωτεύον κλειδί δε μπορεί να τροποποιηθεί
    else:
        j=0 #Σε περίπτωση εισαγωγής νέου αντικειμένου, το πρωτεύον κλειδί πρέπει να μπορεί να εισαχθέι σε entrybox
        sel=['']*len(fields) #Σε περίπτωση εισαγωγής δεδομένων, όλα τα entryboxes πρέπει να εμφανίζονται αρχικά άδεια
    	
    for	i in range(j, len(fields)):
        row = Frame(root)	
        lab = ttk.Label(row, width=12, text=fields[i]+":", anchor='w')	#Όνομα attribute
        ent = Entry(row)	#Entrybox για το attribute
        ent.insert(0,sel[i])	#Εισαγωγή των τωρινών δεδομένων σε περίπτωση που πραγματοποιούμε επεξεργασία
        row.pack(side=TOP, fill	= X, padx = 5, pady=5)	
        lab.pack(side=LEFT)	
        ent.pack(side=RIGHT, expand = YES, fill	= X)	
        entries.append(ent) #Προσθήκη όλων των entry boxes σε μία λίστα
    return entries

#Συνάρτηση ενημέρωσης με το Submit στο παράθυρο επξεργασίας
def savechanges(edit_win, ents,attr_list, sel, ont): #Ents είναι τα entries του παραθύρου επεξεργασίας
    #attr_list η λίστα attributes για το αντικείμενο που επεξεργαζόμαστε, sel είναι οι αρχικές τιμές αυτών των attributes
    #ont η οντότητα του αντικειμένου
    try:
        data=[] #Οι τιμές των entries από το παράθυρο επεξεργασίας
        for i in ents:
            temp=i.get()
            if temp=='':
                temp=None #Αν κάποια τιμή εισόδου είναι ένα κενό str, η είσοδος τίθεται ως None
            data.append(temp)
        diff_att=[] #Attributes που άλλαξαν
        new_val=() #Νέες τιμες
        for i in range(1, len(sel)):
            if str(data[i-1])!=str(sel[i]): #Σύγκριση των αρχικών δεδομένων με τα δεδομένα που υπήρχαν στο παράθυρο επξεργασίας όταν πατήσαμε submit
                #Επειδή στο update δε γίνεται να αλλάξουμε το id, η λίστα data(τιμές των entries που βάλαμε στην επεξεργασία)
                #είναι κατά 1 μικρότερη από τη λίστα των attributes του αντικειμένου που επεξεργαζόμαστε, καθώς "λείπει" το id στην data
                new_val+=(data[i-1],) #Σε περίπτωση που υπάρχει διαφορά, τότε προσθέτουμε στο tuple τη νέα τιμή
                diff_att.append(attr_list[i]) #Προσθήκη του ονόματος του attribute που άλλαξε
        if diff_att!=[]: #Αν έχει υπάρξει κάποια τροποποίηση, δημιουργούμε query για την αποθήκευση της αλλαγής στη βάση
            sql_query="UPDATE "+ont+" SET "+diff_att[0]+"=?"
            i=1
            while i<len(diff_att):
                sql_query+=', '+diff_att[i]+"=?"
                i+=1
            sql_query+=" WHERE "+attr_list[0]+"="+str(sel[0]) #Χρήση του ID ως αναγνωριστικό στο query επεξεργασίας
            c.execute(sql_query, new_val)
            con.commit()
        edit_win.destroy()
    except sqlite3.IntegrityError as err:
        t=str(err)
        x=t.partition(".")
        if x[-1]=='':
            messagebox.showerror('Error', "Constraint failed") #Errorbox σε περίπτωση μη τήρησης κάπου περιορισμού foreign key
        else:
            messagebox.showerror('Error', "'"+x[-1]+"'  value missing/not acceptable") #Errorbox σε περίπτωση κενής/μη έγκυρης τιμής σε συγκεκριμένο πεδίο
        edit_win.lift() #Επαναφορά στο προσκήνιο του παραθύρου επεξεργασίας/εισαγωγής δεδομένων

#Συνάρτηση edit
def edit_sel():
    try:
        i = tree_view.selection()[0] #Δείκτης αντικειμένου που έχει επιλεγεί από το treeview
        sel = tree_view.item(i)['values'] #Οι τιμές του επιλεγμένου αντικειμένου
        attr_list=[] #Λίστα attributes του αντικειμένου
        ont=cbox1.get() #Ανάκτηση οντότητας του αντικειμένου
        c.row_factory = lambda cursor, row: row[0] #STRs αντί για tuples
        c.execute("SELECT name FROM PRAGMA_table_info('"+ont+"')") #Ανάκτηση της λίστας attributes του αντικειμένου
        data=c.fetchall()
        for i in data:
            attr_list.append(i)
        c.row_factory = None        
        edit_win=Tk() #Δημιουργία παραθύρου επεξεργασίας
        add_style(edit_win)
        edit_win.title('Edit Selection')
        ents=makeform(edit_win, attr_list,'edit', sel) #Δημιουργία entryboxes, labels στο παράθυρο επξεργασίας
        #Κουμπιά αποθήκευσης και εξόδου
        sub_btn = ttk.Button(edit_win, text = 'Submit',command=(lambda:savechanges(edit_win, ents, attr_list, sel, ont)))	
        sub_btn.pack(side = LEFT, padx = 5, pady = 5)	
        quit_btn = ttk.Button(edit_win, text = 'Exit', command=edit_win.destroy)	
        quit_btn.pack(side = LEFT, padx = 5,	pady = 5)
        
        edit_win.mainloop()
    except: #Σε περίπτωση μη επιλογής αντικειμένου από το treeview
        pass

#Εισαγωγή δεδομένων με το πάτημα του Submit στο παράθυρο insert
def insert_data(new_win, ents, ont): 
    try:
        data=() #Οι τιμές των entries από το παράθυρο επεξεργασίας
        q='' #Τα ερωτηματικά στο query για το insert
        for i in ents:
            temp=i.get()
            if temp=='':
                temp=None
            data+=(temp,)
            q+='?, '
        q=q[:-2]+");"
        sql_query="INSERT INTO "+ont+" VALUES("+q
        c.execute(sql_query, data)
        con.commit()
        new_win.destroy()
        di={}
        di['Maintenance']='Under_maint'
        di['Guided_Tour']='Is_Presented'
        di['Product']='Inspired_by'
        if ont in di: #Όταν δημιοργούμε μία από τις 3 οντότητες του λεξικού di, εμφανίζεται αυτόματα παράθυρο για τη δημιουργία εγγραφής στους αντίστοιχους πινάκες συσχέτισης
            newont=di[ont] #Τίτλος του πίνακα συσχέτισης
            new_ex(newont, data[0]) #Δημιουργία πίνακα συσχέτισης
    except sqlite3.IntegrityError as err:
        t=str(err)
        x=t.partition(".")
        messagebox.showerror('Error', "'"+x[-1]+"'  value missing/not acceptable") #Εμφάνιση errorbox με τη μη έγκυρη τιμή
        new_win.lift()

#Συνάρτηση insert
def new():
    try:
        attr_list=[]
        ont=cbox1.get() #Ανάκτηση κεντρικής οντότητας
        c.row_factory = lambda cursor, row: row[0] #STRs αντί για tuples
        c.execute("SELECT name FROM PRAGMA_table_info('"+ont+"')") #Ανάκτηση ονομάτων attributes αυτής της οντότητας
        data=c.fetchall()
        for i in data:
            attr_list.append(i)
        c.row_factory = None #Αναίρεση της προηγούμενης αλλαγής για τα tuples
        
        new_win=Tk() #Δημιουργία παραθύρου εισαγωγής δεδομένων
        add_style(new_win)
        new_win.title('New data')
        ents=makeform(new_win, attr_list, 'new') #Διαμόρφωση παραθύρου εισαγωγής δεδομένων
        #Κουμπιά αποθήκευσης και εξόδου
        sub_btn = ttk.Button(new_win, text = 'Submit',command=(lambda:insert_data(new_win, ents, ont)))	
        sub_btn.pack(side = LEFT, padx = 5, pady = 5)	
        quit_btn = ttk.Button(new_win, text = 'Exit', command=new_win.destroy)	
        quit_btn.pack(side = LEFT, padx = 5,	pady = 5)
        new_win.mainloop()
    except: pass

#Συνάρτηση διαγραφής (delete selection) 
def del_sel():
    try:
        ont=cbox1.get() #Ανάκτηση οντότητας
        i = tree_view.selection()[0] #Ανάκτηση επιλεγμένου αντικειμένου
        sel = tree_view.item(i)['values'][0] #Η τιμή κλειδιού του επιλεγμένου αντικειμένου
        
        c.row_factory = lambda cursor, row: row[0] #STRs αντί για tuples
        c.execute("SELECT name FROM PRAGMA_table_info('"+ont+"')") #Attributes αντικειμένου
        data=c.fetchone() #Το όνομα του πρωτεύοντος κλειδιού (που είναι και 1ο attribute)
        c.row_factory = None
        ans=askyesno(title='Delete row', message='Are you sure you want to delete this row?') #Προειδοποιητικό παράθυρο
        if ans: #Αν ο χρήστης αποδεχτεί την προειδοποίηση
            try:
                sql_query="DELETE FROM "+ont+" WHERE "+data+"=?" #query διαγραφής
                c.execute(sql_query, (sel,))
                con.commit()
            except sqlite3.IntegrityError as err: #Έλεγχος για περιορισμούς και εμφάνιση σχετικού μηνμύματος
                t=str(err)
                messagebox.showerror('Error', t)
    except:pass

#Συμπλήρωση του treeview στο παράθυρο επεξεργασίας έκθεσης
def fill_etree(str, id, etree):
    for i in etree.get_children():   #Καθαρισμός του treeview
        etree.delete(i)
    x=(id,) #ID της έκθεσης που διαχειριζόμαστε ως tuple
    if str=='Piece_of_Art': #Αν έχουμε επιλέξει να εμφανίσουμε όλα τα έργα τέχνης της έκθεσης
        query="SELECT AP.ID, AP.Title FROM Shown JOIN Piece_of_Art AS AP ON AP_ID=AP.ID WHERE EXH_ID==?"
        c.execute(query, x)
    else: #Αν έχουμε επιλέξει να εμφανίσουμε όλες τις αίθουσες της έκθεσης
        query="SELECT Room.Number, Room.Title FROM Takes_Place as TP JOIN Room ON TP.Room_Number=Room.Number WHERE TP.EXH_ID==?"
        c.execute(query, x)
    data = c.fetchall() #Ανάκτηση όλων των αποτελεσμάτων από το SQL query
    for row in data: #Εκτύπωση των αποτελεσμάτων στο treeview
        etree.insert('', 'end', values=row)


#Συνάρτηση διαχείρισης έκθεσης (manage exhibition)
def mng():
    try:
        i = tree_view.selection()[0]
        id = tree_view.item(i)['values'][0] #Το id της επιλεγμένης έκθεσης

        #Δημιουργία παραθύρου διαχείρισης
        mng_win=Tk()
        add_style(mng_win)
        mng_win.geometry('600x300') #Διαστάσεις παραθύρου
        frame_view = Frame(mng_win, bg=bg_color)
        frame_view.grid(row=3, column=7, padx=20)
        frame_etree = Frame(mng_win) #Treeview εμφάνισης των αποτελεσμάτων που παίρνουμε στο παράθυρο αυτό
        frame_etree.grid(row=0, column=1, rowspan=6, pady=20, padx=20)
        #Κουμπιά επιλογών
        btn_poa = ttk.Button(frame_view, width=20, text="Show all Art Pieces", command=lambda:fill_etree('Piece_of_Art', id, etree))
        btn_room = ttk.Button(frame_view, width=20, text="Show all Rooms", command=lambda:fill_etree('', id, etree))
        btn_poa.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        btn_room.grid(row=1, column=0, sticky='ew', padx=5)
        btn_add_poa = ttk.Button(frame_view, width=20, text="Add Art Piece", command=lambda:new_ex('Piece_of_Art', id))
        btn_add_room = ttk.Button(frame_view, width=20, text="Add Room", command=lambda: new_ex('Takes_Place', id))
        btn_quit_mng = ttk.Button(frame_view, width=20, text="Quit", command=mng_win.destroy)
        btn_poa.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        btn_add_poa.grid(row=2, column=0, sticky='ew', padx=5)
        btn_room.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        btn_add_room.grid(row=4, column=0, sticky='ew', padx=5)
        btn_quit_mng.grid(row=5, column=0, sticky='ew', padx=5, pady=5)

        #Διαμόρφωση treeview και εισαγωγή scrollbar
        columns = ['id', 'Title']
        etree = ttk.Treeview(frame_etree, columns=columns, show="headings")
        etree.column("id", width=80)
        etree.column('Title', width=200)
        etree.heading('Title', text='Title')
        etree.heading('id', text='ID/No.')
        etree.pack(side="left", fill="y")
        sbar = Scrollbar(frame_etree, orient='vertical')
        sbar.configure(command=etree.yview)
        sbar.pack(side="left", fill="y")
        etree.config(yscrollcommand=sbar.set)
    except: #Σε περίπτωση μη επιλογής αντικειμένου πριν το πάτημα του manage
        pass


#Συνάρτηση για προσθήκη στοιχείου σε μια έκθεση (αίθουσα ή έκθεμα) ή προσθήκη εγγραφής σε άλλο πίνακα συσχέτισης
def new_ex(str, id):
    new_ex_win=Tk() #Δημιουργία νέου παραθύρου για εισαγωγή δεδομένων
    add_style(new_ex_win)
    new_ex_win.title('New data')
    ent_frame=Frame(new_ex_win)
    ent_frame.grid(row=0)
        
    if str=='Piece_of_Art': #Αν το παράθυρο εμφανίστηκε επειδή πατήσαμε Add Art Piece στο μενού διαχείρισης έκθεσης
        txt='Enter the title of the Art Piece'
    
    elif str=='Takes_Place': #Αν το παράθυρο εμφανίστηκε επειδή πατήσαμε Add Room στο μενού διαχείρισης έκθεσης
        txt="Enter the Room's Number"

    elif str=='Inspired_by': #Αν το παράθυρο εμφανίστηκε επειδή δημιουργήσαμε προϊόν
        txt='Enter the title of an art piece by which this product is inspired'

    elif str=='Under_maint': #Αν το παράθυρο εμφανίστηκε επειδή δημιουργήσαμε συντήρηση
        txt='Enter the ID of the art piece to be maintained'

    elif str=='Is_Presented': #Αν το παράθυρο εμφανίστηκε επειδή δημιουργήσαμε ξενάγηση
        txt='Enter the title of an exhibition this tour is going to visit'

    #Διαμόρφωση παραθύρου εισαγωγής δεδομένων (ID ή τίτλου)
    ap_label=Label(ent_frame, text=txt, font=('bold', 12), pady=10, background=bg_color)
    ap_label.pack()
    data_entry=Entry(ent_frame, width=20, font=12)
    data_entry.pack(padx=5)
    sb_btn=ttk.Button(ent_frame, text='Submit', width=10, command=lambda:addval(str, data_entry, id, new_ex_win))
    qt_btn=ttk.Button(ent_frame, text='Quit', command=new_ex_win.destroy, width=10)
    sb_btn.pack(side='left', pady=10, padx=5)
    qt_btn.pack(side='right', pady=10, padx=5) 
        


#Προσθήκη εγγραφής στους πίνακες συσχέτισης
def addval(str, data_entry, id, new_ex_win):
    key=data_entry.get() #Αν η τιμή που λάβαμε στο παράθυρο εισόδου δεν ήταν κενή
    if key!=None and key!='':
        if str=='Piece_of_Art' or str=='Inspired_by' or str=='Is_Presented':
            #Αν το str εισόδου είναι ένα από τα παραπάνω, τότε από την είσοδο που έχει δοθεί (η οποία είναι όνομα/τίτλος)
            #πρέπει να γίνει ανάκτηση ενός σχετικού ID για την δημιουργία της εγγραφής στον πίνακα που θέλουμε
            dict={'Piece_of_Art':'Piece_of_Art', 'Inspired_by':'Piece_of_Art', 'Is_Presented':'Exhibition'}
            try:
                c.execute("SELECT ID FROM "+dict[str]+" WHERE Title=?", (key,))
                data=c.fetchone()
                if str=='Inspired_by': #Στον πίνακα inspired_by η τιμή που εισάγουμε στο προηγούμενο παράθυρο τοποθετείται πρώτη
                    val=((data[0]),(id),)
                else: 
                    val=((id),(data[0]),)
                sql_query="INSERT INTO "+str+" VALUES (?,?)"
                c.execute(sql_query, val)
                con.commit()
                if str=='Piece_of_Art': #Σε περίπτωση που προσθέτουμε πίνακα σε έκθεση, το παράθυρο καταστρέφεται
                    new_ex_win.destroy()
                else: #Σε περίπτωση που προσθέτουμε εγγραφή στους πίνακες  Inspired_by, Is_Presented, το παράθυρο καθαρίζεται και μένει 
                       #ανοιχτό για να μπορεί ο χρήστης να συμπληρώσει περισσότερες εγγραφές
                    messagebox.showinfo('Success', 'Insertion Successful') #Ειδοποίηση ότι ολοκληρώθηκε επιτυχώς η εγγραφή
                    data_entry.delete(0, END)
                    data_entry.insert(0,'')
                    new_ex_win.lift()
            except:
                messagebox.showerror('Error', "Invalid Title") #Errorbox σε περίπτωση εισόδου μη έγκυρου τίτλου
                new_ex_win.lift()

        elif str=='Takes_Place' or str=='Under_maint':
            #Αν το str εισόδου είναι ένα από τα παραπάνω, τότε η είσοδος που έχει δοθεί είναι το σχετικού ID που χρειαζόμαστε
            #για την δημιουργία της εγγραφής στον πίνακα που θέλουμε
            try:
                val=((id),(key),)
                sql_query="INSERT INTO "+str+" VALUES (?,?)"
                c.execute(sql_query, val)
                con.commit()
                data_entry.delete(0, END)
                data_entry.insert(0,'')
                new_ex_win.destroy()
            except:
                messagebox.showerror('Error', "Invalid Number") #Errorbox σε περίπτωση εισόδου μη έγκυρου ID
                new_ex_win.lift()
    else: pass



#Δημιουργία του γραφικού περιβάλλοντος της εφαρμογής
app = Tk() #Εκκίνηση του παραθύρου
add_style(app)
frame_search = Frame(app, bg=bg_color) 
frame_search.grid(row=0, column=0)

#Βασική αναζήτηση με 1 κριτήριο
search_btn = ttk.Label(frame_search, text='Choose entity:', font=('bold', 14))
search_btn.grid(row=0, column=0)
lbl_search = Label(frame_search, text='Search term:', font=('bold', 12), pady=20, background=bg_color)
lbl_search.grid(row=0, column=3, sticky=E)
artist_search_entry = ttk.Entry(frame_search, width=30)
artist_search_entry.grid(row=0, column=4)
showall_btn = ttk.Button(frame_search, text='Show all values', width=14)
showall_btn.grid(row=0, column=8, pady=30)

#Combobox επιλογής οντότητας αναζήτησης
search_btn2= ttk.Button(frame_search, text='Search', width=12, command=search_by)
search_btn2.grid(row=0, column=7, padx=10)
cbox1 = ttk.Combobox(frame_search, values=['Artist', 'Collection','Collector', 'Exhibition', 'Guided_Tour', 'Maintenance', 'Piece_of_art', 'Product', 'Room', 'Worker' ])
cbox1.grid(row=0, column=1)
cbox1.bind('<<ComboboxSelected>>', selected) #Όταν το combobox οντότητας αλλάζει, αλλάζουν οι επιλογές των υπόλοιπων comboboxes

#Combobox κριτηρίου αναζήτησης
cbox2 = ttk.Combobox(frame_search, values=[])
cbox2.grid(row=0, column=6)
lbl_cbox2 = Label(frame_search, text='Choose criterion:', pady=20, padx=5,background=bg_color)
lbl_cbox2.grid(row=0, column=5)

##Στοιχεία για τα σύνθετα queries
#Δανεισμένα έργα
poa_collector_button = ttk.Button(frame_search, text= 'Δανεισμένα έργα', width=18, command=poa_collector_search)
poa_collector_button.grid(row = 6, column= 4)

#Πλήθος έργων ανά συλλογή
count_poa_per_collection_button =  ttk.Button(frame_search, text= '#Έργων ανά συλλογή', width=20, command=count_poa_per_collection)
count_poa_per_collection_button.grid(row = 6, column=5, padx=20)

#Έργα που απουσιάζουν λόγω συντήρησης
maint_poa_button = ttk.Button(frame_search, text= 'Έργα που συντηρούνται', width=22, command=maint_poa)
maint_poa_button.grid(row = 6, column=6, padx=5)

#Επισκέψεις εκθέσεων ανά ξενάγηση
exh_per_tour_button = ttk.Button(frame_search, text= 'Ξενάγηση σε εκθέσεις', width=20, command=exh_per_tour)
exh_per_tour_button.grid(row = 4, column=4)
exh_per_tour_entry = ttk.Entry(frame_search, width=20)
exh_per_tour_entry.grid(row=3, column=4, sticky=S, pady=5)

#Έργα καλλιτέχνη/ών
pieces_of_artist_button = ttk.Button(frame_search, text= 'Έργα καλλιτέχνη', width=20, command=pieces_of_artist)
pieces_of_artist_button.grid(row = 4, column=5)
pieces_of_artist_entry = ttk.Entry(frame_search, width=20)
pieces_of_artist_entry.grid(row=3, column=5,sticky=S, pady=5)

#Έργα τέχνης ανά έκθεση
poa_per_exh_button = ttk.Button(frame_search, text= 'Έργα ανά έκθεση', width=20, command=poa_per_exh)
poa_per_exh_button.grid(row = 4, column=6)
poa_per_exh_entry = ttk.Entry(frame_search, width=20)
poa_per_exh_entry.grid(row=3, column=6, sticky=S, pady=5)

#Στοιχεία για το advanced search
lbl_search = Label(frame_search, text='Advanced Search', font=('bold', 12), pady=20, background=bg_color)
lbl_search.grid(row=2, column=1, sticky=W)
crit1_search_entry = ttk.Entry(frame_search, width=30)
crit1_search_entry.grid(row=3, column=0)
lbl_crit1 = ttk.Label(frame_search, text='Criterion 1')
lbl_crit1.grid(row=3, column=1, padx=5)
crit1_box = ttk.Combobox(frame_search, values=[])
crit1_box.grid(row=3, column=2)

crit2_search_entry = ttk.Entry(frame_search, width=30)
crit2_search_entry.grid(row=4, column=0, pady=5)
lbl_crit2 = ttk.Label(frame_search, text='Criterion 2')
lbl_crit2.grid(row=4, column=1, padx=5)
crit2_box = ttk.Combobox(frame_search, values=[])
crit2_box.grid(row=4, column=2)

crit3_search_entry = ttk.Entry(frame_search, width=30)
crit3_search_entry.grid(row=5, column=0, pady=5)
lbl_crit3 = ttk.Label(frame_search, text='Criterion 3')
lbl_crit3.grid(row=5, column=1, padx=5)
crit3_box = ttk.Combobox(frame_search, values=[])
crit3_box.grid(row=5, column=2)

crit4_search_entry = ttk.Entry(frame_search, width=30)
crit4_search_entry.grid(row=6, column=0, pady=5)
lbl_crit4 = ttk.Label(frame_search, text='Criterion 4')
lbl_crit4.grid(row=6, column=1, padx=5)
crit4_box = ttk.Combobox(frame_search, values=[])
crit4_box.grid(row=6, column=2)
adv_search_btn= ttk.Button(frame_search, text='Advanced Search', width=18, command=adv_search)
adv_search_btn.grid(row=7, column=1, pady=30, padx = 5)

#Treeview αρχικής σελίδας
frame_tree = Frame(app, bg=light_color)
frame_tree.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=30)
columns = ['0', '1', '2', '3', '4', '5', '6', '7','8','9','10'] #11 προεπιλεγμένες στήλες
tree_view = ttk.Treeview(frame_tree, columns=columns, show="headings")
for col in columns:
     tree_view.column(col, width=140)
tree_view.pack(side="left", fill="y")
scrollbar = Scrollbar(frame_tree, orient='vertical')
scrollbar.configure(command=tree_view.yview)
scrollbar.pack(side="left", fill="y")
tree_view.config(yscrollcommand=scrollbar.set)


#Κουμπιά διαχείρισης κάτω από το treeview
frame_crud = Frame(app, bg=bg_color)
frame_crud.grid(row=11, column=0)
insert_btn= ttk.Button(frame_crud, text='Insert', width=14)
insert_btn.grid(row=0, column=0, pady=10, padx=40)
edit_btn= ttk.Button(frame_crud, text='Edit selection', width=14, command=edit_sel)
edit_btn.grid(row=0, column=1, pady=10)
delete_btn= ttk.Button(frame_crud, text='Delete selection', width=14, command=del_sel)
delete_btn.grid(row=0, column=2, pady=10, padx=40)
manage_btn= ttk.Button(frame_crud, text='Manage exhibition', width=18, command=mng)
manage_btn.grid(row=0, column=3, pady=10)
run_query_btn =ttk.Button(frame_crud, text='Run a query', width=14, command=runquery)
run_query_btn.grid(row=0, column=4, padx=40)
close_btn = ttk.Button(frame_crud, text='Close', width=14, command=close)
close_btn.grid(row=0, column=5)

#Ρυθμίσεις παραθύρου
app.title('Εφαρμογή Πινακοθήκης - Ομάδα 18')
app.geometry('1600x900')

#Εκκίνηση event loop ώστε η εφαρμογή να ανταποκρίνεται σε αλλαγές
app.mainloop()