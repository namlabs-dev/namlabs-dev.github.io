"""The three later techniques (box-line reduction, hidden pairs, naked triples) in every language.

Merged into each language's T by build.py. Links use PFX for the language prefix.
"""

EN = {
    'tech': {
        'box-line-reduction': {
            'name': 'Box-line reduction', 'level': 'medium',
            'card': "A row's only spots for a digit sit in one box: clear the rest of the box.",
            'title': 'Box-Line Reduction in Sudoku: Explained With an Example | namlabs',
            'h1': 'Box-line reduction',
            'desc': 'Box-line reduction: when a digit in a Sudoku row or column can only go inside one box, erase it from the rest of that box. Explained step by step.',
            'lead': 'The mirror image of pointing pairs. If a row can only hold a digit inside one box, that box keeps its copy in that row, and the rest of the box can drop it.',
            'body': '''<h2>What is box-line reduction?</h2>
<p>Every row needs each digit once. Suppose that in one row, a digit can only go in cells that all lie inside the same box. Then the row's copy of the digit will be in that box, and that is the box's copy as well. So the digit cannot appear anywhere else in the box, which means you can erase it from the box's other two rows.</p>
<p><a href="PFXsudoku/techniques/pointing-pairs.html">Pointing pairs</a> work from the box towards the line. Box-line reduction works from the line towards the box. Same idea, opposite direction.</p>

<h2>Example</h2>
[[box-line]]
<p>Look at digit 4 in row 1. The right side of the row is already filled, and the 4 in R5C3 rules out R1C3. That leaves <strong>R1C1 and R1C2</strong>, both inside the top-left box.</p>
<p>So the 4 of row 1 is in that box, and the box already has its 4. Erase 4 from the box's other cells: R2C1, R2C2, R3C1 and R3C2. (R2C3 and R3C3 were already out because of the 4 in column 3.)</p>

<h2>How to find it</h2>
<ol>
<li>Pick a row (or column) and a digit it does not have yet.</li>
<li>List the cells in that row where the digit can still go.</li>
<li>If they all sit in one box, erase the digit from the other cells of that box.</li>
</ol>

<div class="note"><strong>Tip:</strong> if you found pointing pairs but the board is still stuck, flip the view: look along rows and columns instead of inside boxes.</div>

<h2>Where it fits</h2>
<p>Use it together with <a href="PFXsudoku/techniques/pointing-pairs.html">pointing pairs</a>, and before the bigger patterns. When a digit's spots form a tidy rectangle across two lines, try <a href="PFXsudoku/techniques/x-wing.html">X-Wing</a>.</p>''',
        },
        'hidden-pair': {
            'name': 'Hidden pair', 'level': 'medium',
            'card': 'Two digits that fit in only two cells: those cells belong to them.',
            'title': 'Hidden Pairs in Sudoku: How to Spot Them, With Example | namlabs',
            'h1': 'Hidden pair',
            'desc': 'A hidden pair is two digits that can only go in the same two cells of a house. Learn how to find hidden pairs in Sudoku and clear the other candidates.',
            'lead': 'A naked pair is easy to see because two cells show the same two candidates. A hidden pair is the sneaky version: the two digits hide among other candidates.',
            'body': '''<h2>What is a hidden pair?</h2>
<p>Pick a row, column or box and look at where two digits can go. If both digits fit in exactly the same two cells, and nowhere else in the house, those two cells must hold those two digits. So every other candidate in those two cells can be erased.</p>
<p>The cells look crowded, with extra candidates, but those extras are impossible. That is why the pair is "hidden".</p>

<h2>Example</h2>
[[hidden-pair]]
<p>In row 1, the digit 5 can only go in <strong>R1C1 or R1C9</strong>. The digit 6 fits in the same two cells and nowhere else in the row. So one of these cells is 5 and the other is 6.</p>
<p>That means R1C1 and R1C9 cannot be anything else. Erase 1 and 8 from R1C1, and 1, 4 and 8 from R1C9. Both cells are now plain {5, 6}.</p>

<h2>How to find hidden pairs</h2>
<ol>
<li>Pick a house with several empty cells and write the candidates.</li>
<li>For each digit, count the cells where it fits. Note the digits with exactly two spots.</li>
<li>If two digits share the very same two cells, you have a hidden pair.</li>
<li>Erase every other candidate from those two cells.</li>
</ol>

<div class="note"><strong>Tip:</strong> a hidden pair and a naked pair are two sides of one idea. If the leftover cells of the house make a pair or triple on their own, it can be quicker to find that instead.</div>

<h2>Where it fits</h2>
<p>If you already know <a href="PFXsudoku/techniques/naked-pairs.html">naked pairs</a>, this is the natural next step. After it, learn <a href="PFXsudoku/techniques/naked-triple.html">naked triples</a>, which extend the idea to three cells.</p>''',
        },
        'naked-triple': {
            'name': 'Naked triple', 'level': 'hard',
            'card': 'Three cells share three digits: clear them from the rest of the house.',
            'title': 'Naked Triples in Sudoku: Rules and Worked Example | namlabs',
            'h1': 'Naked triple',
            'desc': 'A naked triple is three cells in one house whose candidates come from the same three digits. Learn how to find naked triples in Sudoku, with a worked example.',
            'lead': 'Three cells, three digits. If the candidates of three cells in a house use only the same three digits, those digits are used up, and the rest of the house can drop them.',
            'body': '''<h2>What is a naked triple?</h2>
<p>It is a <a href="PFXsudoku/techniques/naked-pairs.html">naked pair</a> with one more cell. Suppose three cells in a row can only hold 3, 7 and 9. One cell is 3, one is 7, one is 9. No other cell in that row can be any of these digits.</p>
<p>The cells do not need all three candidates each. Combinations such as {3, 9}, {7, 9} and {3, 7} work, and so does {3, 7, 9} in one cell as long as the three cells together use only three digits.</p>

<h2>Example</h2>
[[naked-triple]]
<p>Row 1 has three cells with the candidates <strong>{3, 9}, {7, 9} and {3, 7}</strong>. Together they use only the digits 3, 7 and 9, so those digits belong to these three cells.</p>
<p>Erase 3, 7 and 9 from the rest of row 1. R1C7 goes from {1, 3, 6, 7, 9} to {1, 6}. R1C8 and R1C9 shrink to {1, 2, 6} each, which brings the next move much closer.</p>

<h2>How to find naked triples</h2>
<ol>
<li>Write the candidates in a house with five or more empty cells.</li>
<li>Look for cells that hold two or three candidates.</li>
<li>Find three of them whose candidates add up to just three different digits.</li>
<li>Erase those digits from every other cell in the house.</li>
</ol>

<div class="note"><strong>Tip:</strong> check that the three cells really use only three digits in total. If a fourth digit appears in any of them, it is not a triple.</div>

<h2>Where it fits</h2>
<p>Naked triples are rarer than pairs, but they show up on hard puzzles when pairs and <a href="PFXsudoku/techniques/pointing-pairs.html">pointing pairs</a> have run out. After this, try <a href="PFXsudoku/techniques/x-wing.html">X-Wing</a>.</p>''',
        },
    },
    'boards': {
        'box-line': ('Sudoku grid. In row 1, 4 can only go in R1C1 or R1C2, both in the top-left box, so 4 is removed from R2C1, R2C2, R3C1 and R3C2.',
                     "Row 1's 4 is in the top-left box, so the box's other cells drop 4."),
        'hidden-pair': ('Sudoku grid. In row 1, the digits 5 and 6 can only go in R1C1 and R1C9, so every other candidate is removed from those two cells.',
                        '5 and 6 fit only in R1C1 and R1C9, so those cells keep only 5 and 6.'),
        'naked-triple': ('Sudoku grid. Three cells in row 1 hold the candidates {3, 9}, {7, 9} and {3, 7}, so 3, 7 and 9 are removed from the rest of the row.',
                         'Three cells use only 3, 7 and 9, so the rest of row 1 cannot.'),
    },
    'hub': {
        'desc': 'Learn the Sudoku techniques that solve almost every puzzle: singles, naked and hidden pairs, pointing pairs, box-line reduction, naked triples and X-Wing, each with a worked example.',
        'lead': 'Every Sudoku can be solved by logic. These eight techniques, learned in this order, take you from your first easy puzzle to expert grids.',
    },
}

VI = {
    'tech': {
        'box-line-reduction': {
            'name': 'Thu gọn khối-hàng', 'level': 'medium',
            'card': 'Một hàng chỉ đặt được số trong một khối: xóa khỏi phần còn lại của khối.',
            'title': 'Box-Line Reduction trong Sudoku: giải thích kèm ví dụ | namlabs',
            'h1': 'Thu gọn khối-hàng (Box-Line Reduction)',
            'desc': 'Box-line reduction: khi một số trong hàng hoặc cột Sudoku chỉ đặt được trong một khối, hãy xóa nó khỏi phần còn lại của khối. Giải thích từng bước.',
            'lead': 'Đây là phiên bản ngược của cặp chỉ hướng. Nếu một hàng chỉ đặt được một số trong một khối, khối đó đã dùng số ấy ở hàng này, và phần còn lại của khối không cần số đó nữa.',
            'body': '''<h2>Box-line reduction là gì?</h2>
<p>Mỗi hàng cần đủ mỗi số một lần. Giả sử trong một hàng, một số chỉ có thể nằm ở các ô cùng thuộc một khối. Vậy số của hàng đó nằm trong khối này, và cũng chính là số của khối. Do đó số này không thể xuất hiện ở bất kỳ chỗ nào khác trong khối, nên bạn có thể xóa nó khỏi hai hàng còn lại của khối.</p>
<p><a href="PFXsudoku/techniques/pointing-pairs.html">Cặp chỉ hướng</a> đi từ khối ra hàng. Box-line reduction đi từ hàng vào khối. Cùng một ý tưởng, ngược chiều nhau.</p>

<h2>Ví dụ</h2>
[[box-line]]
<p>Xét số 4 ở hàng 1. Phần bên phải của hàng đã được điền, và số 4 ở H5C3 loại ô H1C3. Còn lại <strong>H1C1 và H1C2</strong>, cả hai nằm trong khối trên cùng bên trái.</p>
<p>Vậy số 4 của hàng 1 nằm trong khối này, và khối đã có số 4 rồi. Hãy xóa 4 khỏi các ô khác của khối: H2C1, H2C2, H3C1 và H3C2. (H2C3 và H3C3 đã bị loại từ trước vì số 4 ở cột 3.)</p>

<h2>Cách tìm</h2>
<ol>
<li>Chọn một hàng (hoặc cột) và một số mà hàng đó chưa có.</li>
<li>Liệt kê các ô trong hàng còn có thể đặt số đó.</li>
<li>Nếu tất cả nằm trong một khối, hãy xóa số đó khỏi các ô khác của khối.</li>
</ol>

<div class="note"><strong>Mẹo:</strong> nếu đã tìm cặp chỉ hướng mà bảng vẫn bí, hãy đổi cách nhìn: nhìn dọc theo hàng và cột thay vì nhìn trong khối.</div>

<h2>Khi nào dùng</h2>
<p>Dùng cùng <a href="PFXsudoku/techniques/pointing-pairs.html">cặp chỉ hướng</a>, trước các mẫu lớn hơn. Khi các chỗ đặt của một số tạo thành hình chữ nhật qua hai hàng, hãy thử <a href="PFXsudoku/techniques/x-wing.html">X-Wing</a>.</p>''',
        },
        'hidden-pair': {
            'name': 'Cặp ẩn', 'level': 'medium',
            'card': 'Hai số chỉ vừa hai ô: hai ô đó thuộc về chúng.',
            'title': 'Cặp ẩn (Hidden Pair) trong Sudoku: cách nhận ra, kèm ví dụ | namlabs',
            'h1': 'Cặp ẩn (Hidden Pair)',
            'desc': 'Cặp ẩn là hai số chỉ đặt được trong cùng hai ô của một nhà. Học cách tìm cặp ẩn trong Sudoku và xóa các ứng viên còn lại.',
            'lead': 'Cặp lộ dễ thấy vì hai ô cùng có hai ứng viên giống nhau. Cặp ẩn thì kín đáo hơn: hai số ẩn mình giữa những ứng viên khác.',
            'body': '''<h2>Cặp ẩn là gì?</h2>
<p>Chọn một hàng, cột hoặc khối và xem hai số có thể đặt ở đâu. Nếu cả hai số chỉ vừa đúng cùng hai ô, và không ở đâu khác trong nhà, thì hai ô đó phải chứa đúng hai số này. Vậy mọi ứng viên khác trong hai ô đó đều xóa được.</p>
<p>Hai ô trông "đông đúc" vì có thêm ứng viên, nhưng các ứng viên thừa đó là không thể. Vì thế cặp này gọi là "ẩn".</p>

<h2>Ví dụ</h2>
[[hidden-pair]]
<p>Ở hàng 1, số 5 chỉ có thể nằm ở <strong>H1C1 hoặc H1C9</strong>. Số 6 cũng chỉ vừa đúng hai ô này và không ở đâu khác trong hàng. Vậy một ô là 5 và ô kia là 6.</p>
<p>Nghĩa là H1C1 và H1C9 không thể là số nào khác. Hãy xóa 1 và 8 khỏi H1C1, xóa 1, 4 và 8 khỏi H1C9. Hai ô giờ chỉ còn {5, 6}.</p>

<h2>Cách tìm cặp ẩn</h2>
<ol>
<li>Chọn một nhà còn nhiều ô trống và ghi ứng viên.</li>
<li>Với mỗi số, đếm số ô mà nó vừa. Ghi lại các số chỉ có đúng hai chỗ.</li>
<li>Nếu hai số có chung đúng hai ô, đó là cặp ẩn.</li>
<li>Xóa mọi ứng viên khác khỏi hai ô đó.</li>
</ol>

<div class="note"><strong>Mẹo:</strong> cặp ẩn và cặp lộ là hai mặt của cùng một ý tưởng. Nếu những ô còn lại của nhà tự tạo thành một cặp hay bộ ba, có khi tìm chúng nhanh hơn.</div>

<h2>Khi nào dùng</h2>
<p>Nếu bạn đã biết <a href="PFXsudoku/techniques/naked-pairs.html">cặp lộ</a>, đây là bước tiếp theo tự nhiên. Sau đó hãy học <a href="PFXsudoku/techniques/naked-triple.html">bộ ba lộ</a>, mở rộng ý tưởng sang ba ô.</p>''',
        },
        'naked-triple': {
            'name': 'Bộ ba lộ', 'level': 'hard',
            'card': 'Ba ô chung ba số: xóa chúng khỏi phần còn lại của nhà.',
            'title': 'Bộ ba lộ (Naked Triple) trong Sudoku: quy tắc và ví dụ | namlabs',
            'h1': 'Bộ ba lộ (Naked Triple)',
            'desc': 'Bộ ba lộ là ba ô trong một nhà có ứng viên chỉ thuộc cùng ba số. Học cách tìm bộ ba lộ trong Sudoku, kèm ví dụ.',
            'lead': 'Ba ô, ba số. Nếu ứng viên của ba ô trong một nhà chỉ dùng cùng ba số, ba số đó đã hết chỗ, và phần còn lại của nhà có thể bỏ chúng.',
            'body': '''<h2>Bộ ba lộ là gì?</h2>
<p>Đó là <a href="PFXsudoku/techniques/naked-pairs.html">cặp lộ</a> thêm một ô. Giả sử ba ô trong một hàng chỉ có thể là 3, 7 và 9. Một ô là 3, một ô là 7, một ô là 9. Không ô nào khác trong hàng đó có thể là các số này.</p>
<p>Mỗi ô không cần đủ cả ba ứng viên. Các tổ hợp như {3, 9}, {7, 9} và {3, 7} đều được, miễn là cả ba ô cộng lại chỉ dùng ba số.</p>

<h2>Ví dụ</h2>
[[naked-triple]]
<p>Hàng 1 có ba ô với ứng viên <strong>{3, 9}, {7, 9} và {3, 7}</strong>. Gộp lại chỉ có ba số 3, 7 và 9, nên ba số này thuộc về ba ô đó.</p>
<p>Hãy xóa 3, 7 và 9 khỏi phần còn lại của hàng 1. H1C7 từ {1, 3, 6, 7, 9} còn {1, 6}. H1C8 và H1C9 còn {1, 2, 6}, đưa bạn đến gần nước đi tiếp theo.</p>

<h2>Cách tìm bộ ba lộ</h2>
<ol>
<li>Ghi ứng viên trong một nhà còn từ năm ô trống trở lên.</li>
<li>Tìm các ô có hai hoặc ba ứng viên.</li>
<li>Chọn ba ô mà ứng viên gộp lại chỉ có ba số khác nhau.</li>
<li>Xóa ba số đó khỏi mọi ô khác trong nhà.</li>
</ol>

<div class="note"><strong>Mẹo:</strong> hãy kiểm tra ba ô thật sự chỉ dùng tổng cộng ba số. Nếu có số thứ tư xuất hiện ở bất kỳ ô nào, đó không phải bộ ba.</div>

<h2>Khi nào dùng</h2>
<p>Bộ ba lộ hiếm hơn cặp, nhưng xuất hiện ở đề khó khi cặp và <a href="PFXsudoku/techniques/pointing-pairs.html">cặp chỉ hướng</a> đã hết. Sau bài này, hãy thử <a href="PFXsudoku/techniques/x-wing.html">X-Wing</a>.</p>''',
        },
    },
    'boards': {
        'box-line': ('Bảng Sudoku. Ở hàng 1, số 4 chỉ đặt được ở H1C1 hoặc H1C2, cùng trong khối trên bên trái, nên 4 bị xóa khỏi H2C1, H2C2, H3C1 và H3C2.',
                     'Số 4 của hàng 1 nằm trong khối trên bên trái, nên các ô khác của khối bỏ 4.'),
        'hidden-pair': ('Bảng Sudoku. Ở hàng 1, số 5 và 6 chỉ đặt được ở H1C1 và H1C9, nên mọi ứng viên khác bị xóa khỏi hai ô này.',
                        '5 và 6 chỉ vừa H1C1 và H1C9, nên hai ô chỉ còn 5 và 6.'),
        'naked-triple': ('Bảng Sudoku. Ba ô ở hàng 1 có ứng viên {3, 9}, {7, 9} và {3, 7}, nên 3, 7 và 9 bị xóa khỏi phần còn lại của hàng.',
                         'Ba ô chỉ dùng 3, 7 và 9, nên phần còn lại của hàng 1 không thể có chúng.'),
    },
    'hub': {
        'desc': 'Học các kỹ thuật giải gần như mọi đề Sudoku: ô đơn, cặp lộ, cặp ẩn, cặp chỉ hướng, box-line reduction, bộ ba lộ và X-Wing, mỗi kỹ thuật có ví dụ minh họa.',
        'lead': 'Mọi đề Sudoku đều giải được bằng suy luận. Học tám kỹ thuật này theo thứ tự, bạn sẽ đi từ đề dễ đầu tiên đến các bảng chuyên gia.',
    },
}

JA = {
    'tech': {
        'box-line-reduction': {
            'name': 'ボックス・ライン・リダクション', 'level': 'medium',
            'card': '行の中でその数字が入るのが1つのブロックだけなら、ブロックの残りから消せます。',
            'title': 'ボックス・ライン・リダクション：ナンプレの候補を減らす技 | namlabs',
            'h1': 'ボックス・ライン・リダクション',
            'desc': '行や列でその数字が入る場所が1つのブロックの中だけなら、ブロックのほかのマスから消せます。例題つきで解説します。',
            'lead': 'ポインティングペアの逆の考え方です。行の中でその数字が入る場所が1つのブロックにしかなければ、そのブロックの残りのマスからは消せます。',
            'body': '''<h2>ボックス・ライン・リダクションとは</h2>
<p>どの行にも各数字は1つ入ります。ある行で、その数字が入れるマスがすべて同じブロックの中にあるとします。すると、その行の数字はこのブロックの中にあり、それがそのままブロックの数字になります。ブロックのほかのマスには入れないので、ほかの2行から消せます。</p>
<p><a href="PFXsudoku/techniques/pointing-pairs.html">ポインティングペア</a>はブロックからラインへ、これはラインからブロックへ。同じ考え方の逆向きです。</p>

<h2>例題</h2>
[[box-line]]
<p>1行目の4に注目します。行の右側はもう埋まっていて、R5C3 の4が R1C3 を除外します。残るのは、どちらも左上のブロックにある <strong>R1C1 と R1C2</strong> です。</p>
<p>つまり1行目の4はこのブロックの中にあります。ブロックのほかのマス R2C1、R2C2、R3C1、R3C2 から4を消せます。（R2C3 と R3C3 は3列目の4で、すでに除外されています。）</p>

<h2>見つけ方</h2>
<ol>
<li>行（または列）と、まだ入っていない数字を選びます。</li>
<li>その行でまだその数字が入るマスを書き出します。</li>
<li>すべてが1つのブロックにあれば、そのブロックのほかのマスから消します。</li>
</ol>

<div class="note"><strong>コツ：</strong>ポインティングペアを探しても詰まったら、見方を変えてみましょう。ブロックの中ではなく、行と列に沿って探します。</div>

<h2>どんなときに使う？</h2>
<p><a href="PFXsudoku/techniques/pointing-pairs.html">ポインティングペア</a>とセットで使い、大きなパターンの前に試します。数字の入る場所が2本のラインにまたがる長方形になったら、<a href="PFXsudoku/techniques/x-wing.html">X-Wing</a>を探しましょう。</p>''',
        },
        'hidden-pair': {
            'name': '隠れたペア', 'level': 'medium',
            'card': '2つの数字が入るのが同じ2マスだけ。その2マスはその数字のもの。',
            'title': '隠れたペア（Hidden Pair）：見つけ方と例題 | namlabs',
            'h1': '隠れたペア（Hidden Pair）',
            'desc': '隠れたペアは、同じハウスの同じ2マスにしか入らない2つの数字のこと。ナンプレでの見つけ方と、ほかの候補の消し方を解説します。',
            'lead': '裸のペアは、2マスが同じ2つの候補を持つので見つけやすい形です。隠れたペアは、2つの数字がほかの候補に紛れているタイプです。',
            'body': '''<h2>隠れたペアとは</h2>
<p>行・列・ブロックで、2つの数字が入る場所を調べます。2つとも、ハウスの中でまったく同じ2マスにしか入らないなら、その2マスはその2つの数字で決まりです。2マスにあるほかの候補はすべて消せます。</p>
<p>2マスには余分な候補があって混み合って見えますが、それらは入れません。だから「隠れた」ペアと呼びます。</p>

<h2>例題</h2>
[[hidden-pair]]
<p>1行目で、5が入るのは <strong>R1C1 か R1C9</strong> だけ。6も同じ2マスにしか入りません。つまり片方が5、もう片方が6です。</p>
<p>だから R1C1 と R1C9 はほかの数字になれません。R1C1 から1と8を、R1C9 から1・4・8を消します。2マスとも {5, 6} だけになります。</p>

<h2>隠れたペアの見つけ方</h2>
<ol>
<li>空きの多いハウスを選び、候補を書き込みます。</li>
<li>数字ごとに、入れるマスの数を数えます。ちょうど2マスの数字に印をつけます。</li>
<li>2つの数字が同じ2マスを共有していれば、隠れたペアです。</li>
<li>その2マスから、ほかの候補をすべて消します。</li>
</ol>

<div class="note"><strong>コツ：</strong>隠れたペアと裸のペアは、同じ考え方の表と裏です。ハウスの残りのマスがペアやトリプルになっているなら、そちらを探すほうが早いこともあります。</div>

<h2>どんなときに使う？</h2>
<p><a href="PFXsudoku/techniques/naked-pairs.html">裸のペア</a>を覚えたら、次はこれ。そのあとは3マスに広げた<a href="PFXsudoku/techniques/naked-triple.html">裸のトリプル</a>へ進みましょう。</p>''',
        },
        'naked-triple': {
            'name': '裸のトリプル', 'level': 'hard',
            'card': '3マスが3つの数字を共有。ハウスのほかのマスから消せます。',
            'title': '裸のトリプル（Naked Triple）：ルールと例題 | namlabs',
            'h1': '裸のトリプル（Naked Triple）',
            'desc': '裸のトリプルは、同じハウスの3マスの候補が同じ3つの数字だけからなる形。ナンプレでの見つけ方を例題つきで解説します。',
            'lead': '3マス、3つの数字。ハウスの3マスの候補が同じ3つの数字だけなら、その数字は使い切り。ハウスのほかのマスからは消せます。',
            'body': '''<h2>裸のトリプルとは</h2>
<p><a href="PFXsudoku/techniques/naked-pairs.html">裸のペア</a>にマスを1つ足した形です。行の3マスが、3・7・9にしかならないとします。1つが3、1つが7、1つが9。その行のほかのマスは、この数字にはなれません。</p>
<p>3マスがそれぞれ3つの候補を持つ必要はありません。{3, 9}、{7, 9}、{3, 7} のような組み合わせでも、3マス合わせて3つの数字だけなら成立します。</p>

<h2>例題</h2>
[[naked-triple]]
<p>1行目に、候補が <strong>{3, 9}、{7, 9}、{3, 7}</strong> の3マスがあります。合わせても3・7・9だけなので、この3つの数字はこの3マスのものです。</p>
<p>1行目のほかのマスから3・7・9を消します。R1C7 は {1, 3, 6, 7, 9} から {1, 6} に。R1C8 と R1C9 は {1, 2, 6} になり、次の手がぐっと近づきます。</p>

<h2>裸のトリプルの見つけ方</h2>
<ol>
<li>空きが5マス以上のハウスに候補を書き込みます。</li>
<li>候補が2つか3つのマスを探します。</li>
<li>3マスの候補を合わせて、異なる数字がちょうど3つになる組を探します。</li>
<li>その3つの数字を、ハウスのほかのマスから消します。</li>
</ol>

<div class="note"><strong>コツ：</strong>3マス合わせて本当に3つの数字だけか確かめましょう。4つ目の数字が1マスにでもあれば、トリプルではありません。</div>

<h2>どんなときに使う？</h2>
<p>ペアより数は少ないですが、ペアや<a href="PFXsudoku/techniques/pointing-pairs.html">ポインティングペア</a>が尽きた難問で出てきます。次は<a href="PFXsudoku/techniques/x-wing.html">X-Wing</a>に挑戦しましょう。</p>''',
        },
    },
    'boards': {
        'box-line': ('ナンプレの盤面。1行目で4が入るのは、どちらも左上のブロックにある R1C1 か R1C2 だけなので、R2C1・R2C2・R3C1・R3C2 から4を消します。',
                     '1行目の4は左上のブロックにあるので、ブロックのほかのマスから4が消える。'),
        'hidden-pair': ('ナンプレの盤面。1行目で5と6が入るのは R1C1 と R1C9 だけなので、この2マスからほかの候補をすべて消します。',
                        '5と6は R1C1 と R1C9 にしか入らないので、2マスには5と6だけが残る。'),
        'naked-triple': ('ナンプレの盤面。1行目の3マスの候補が {3, 9}、{7, 9}、{3, 7} なので、行のほかのマスから3・7・9を消します。',
                         '3マスが3・7・9だけを使うので、1行目のほかのマスには入らない。'),
    },
    'hub': {
        'desc': 'ほぼすべてのナンプレが解けるテクニックを紹介：シングル、裸のペア、隠れたペア、ポインティングペア、ボックス・ライン・リダクション、裸のトリプル、X-Wing。例題つき。',
        'lead': 'ナンプレはどれも論理で解けます。この8つのテクニックを順番に覚えれば、最初の簡単な問題から上級者向けの盤面まで進めます。',
    },
}


def merge(texts):
    """Adds the extra techniques to {'en': T, ...}."""
    for lang, extra in (('en', EN), ('vi', VI), ('ja', JA)):
        t = texts[lang]
        pfx = '/' if lang == 'en' else f'/{lang}/'
        for k, v in extra['tech'].items():
            t['tech'][k] = {f: (s.replace('PFX', pfx) if isinstance(s, str) else s) for f, s in v.items()}
        t['boards'].update(extra['boards'])
        t['hub'].update(extra['hub'])
