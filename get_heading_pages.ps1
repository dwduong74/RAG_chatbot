$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "C:\project\NCKH\RAG\BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.docx"

if (Test-Path $docPath) {
    $doc = $word.Documents.Open($docPath)
    Write-Host "Updating document fields..."
    $doc.Fields.Update()
    
    Write-Host "Document Page Count: $($doc.ComputeStatistics(2))" # 2 = wdStatisticPages
    
    # Check page numbers of headings
    foreach ($p in $doc.Paragraphs) {
        $text = $p.Range.Text.Trim()
        if ($text -match "^(CHƯƠNG|THÔNG TIN|LỜI CAM ĐOAN|LỜI CẢM ƠN|MỤC LỤC|DANH MỤC|TÓM TẮT|TÀI LIỆU THAM KHẢO|PHỤ LỤC|\d+\.\d+)") {
            $page = $p.Range.Information(1) # 1 = wdActiveEndPageNumber
            if ($text.Length -lt 80) {
                Write-Host "[$page] $text"
            }
        }
    }
    
    $doc.Close($false)
} else {
    Write-Host "File not found: $docPath"
}
$word.Quit()
