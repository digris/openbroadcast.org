from navutils import menu

main_menu = menu.Menu("main")
menu.register(main_menu)


library = menu.Node(id="library", label="Library", pattern_name="library:media-list")
main_menu.register(library)
