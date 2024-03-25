import box_patern
import machine
import paterns
import flet as ft
import export


glob = {}

def cal(e):
    if not (b_y.value and b_z.value and b_t.value and b_x.value):
        return
    mult = {'X': float(b_x.value),
            'Y': float(b_y.value),
            'Z': float(b_z.value),
            'T': float(b_t.value),
            }
    glob['box'] = box_patern.BoxPatern(**paterns.basic_box_patern)
    glob['box'].calculate_box(**mult)
    tf.value = f'Size of cutoff: {glob['box'].size[0]} X {glob['box'].size[1]}'
    if glob['machine'].size_x < glob['box'].size[0] or glob['machine'].size_y < glob['box'].size[1]:
        tf.value = f'Too big to fit in machine area: {glob['box'].size[0]} X {glob['box'].size[1]}'
    tf.update()
    but.disabled = False
    but.update()
    draw(None)
def next_field(e):
    if not b_x.value:
        b_x.focus()
    elif not b_y.value:
        b_y.focus()
    elif not b_z.value:
        b_z.focus()
    elif not b_t.value:
        b_t.focus()
    else: cal(None)

def export_box(e):
    pol = glob['box'].cut + glob['box'].fold
    export.make_dxf(pol)



def path_finder(polylines, scale):
    paths = []
    for p in polylines:
        scaled_vertices = list(map(lambda x: [x[0]*scale, x[1]*scale], p.vertices))
        paths.append(ft.canvas.Path.MoveTo(*scaled_vertices[0]))
        for pa in scaled_vertices[1:-1]:
            paths.append(ft.canvas.Path.LineTo(*pa))
        paths.append(ft.canvas.Path.LineTo(*scaled_vertices[-1]))
    return paths


def draw(e):
    if e is not None:
        glob['width'] = e.width
        glob['height'] = e.height

    if not (b_y.value and b_z.value and b_t.value and b_x.value):
        return
    scale_x = glob['width'] / glob['machine'].size_x
    scale_y = glob['height'] / glob['machine'].size_y
    scale = min(scale_x, scale_y)
    cut = ft.canvas.Path(elements=path_finder(glob['box'].cut, scale), paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE,color=ft.colors.SECONDARY))
    fold = ft.canvas.Path(elements=path_finder(glob['box'].fold, scale), paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE,color=ft.colors.ERROR))
    area = ft.canvas.Path(elements=path_finder(glob['machine'].work_area, scale), paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE, color=ft.colors.PRIMARY))
    cv.shapes = [cut, fold, area]
    cv.update()


b_x = ft.TextField(label='Lenght', keyboard_type='NUMBER', input_filter=ft.NumbersOnlyInputFilter(), on_blur=cal, on_submit=next_field)
b_y = ft.TextField(label='Width', keyboard_type='NUMBER', input_filter=ft.NumbersOnlyInputFilter(), on_blur=cal, on_submit=next_field)
b_z = ft.TextField(label='Heigh', keyboard_type='NUMBER', input_filter=ft.NumbersOnlyInputFilter(), on_blur=cal, on_submit=next_field)
b_t = ft.TextField(label='Thicness', keyboard_type='NUMBER', input_filter=ft.NumbersOnlyInputFilter(), on_blur=cal, on_submit=next_field)
cv = ft.canvas.Canvas(on_resize=draw, width=(float('inf')), expand=True)
tf = ft.Text('Add all parameters')
but = ft.ElevatedButton(text='Create DXF', disabled=True, on_click=export_box)

def main(page:ft.Page):
    page.add(ft.Row(controls=[b_x, b_y, b_z, b_t]))
    page.add(cv)
    page.add(tf)
    page.add(but)
    glob['machine'] = machine.Machine('lazer', 1500, 1000, None, None)

    page.padding = 5




if __name__ == '__main__':
    ft.app(target=main)


