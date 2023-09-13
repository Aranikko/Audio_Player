from flet import *

def main(page: Page):
    
    space = [page.add(Text(' ')) for i in range(21)]
    
    page.add(
		
		Row(
			[
				IconButton(icon=icons.PLAY_ARROW),
				IconButton(icon=icons.PLAY_ARROW),
			],
			wrap=False,
			spacing=0,
			alignment=MainAxisAlignment.CENTER,
		)
  
	)
    
app(target=main)