(load #P"C:/HOME/quicklisp/setup.lisp")
(ql:quickload "cl-csv")
(print "_______START DATA_______")
(setq gameData (cl-csv:read-csv #P"normalData.csv"))
(print gameData)
(setq data (cdr gameData))

(setq linearData `(0 0))
(setq countlen 0)
(mapcar (lambda (el) 
    (setq tmp_list (parse-integer(car el)))
    (setq tmp_list (cons tmp_list (+ (parse-integer(cadr el)) (/ (parse-integer(cadddr el)) (parse-integer(caddr el))) )))
    (if (equal countlen 0) (setq linearData tmp_list) (if (equal countlen 1) (setq linearData (list linearData tmp_list)) (setq linearData (append linearData (list tmp_list)))) )
    (setq countlen (+ countlen 1))
) data)
(print "_______DATA TO PROCESING_______")
(print linearData)

(setq dataLen (length linearData))
(setq mean-x 0)
(setq mean-y 0)
(setq ss-xy 0)
(setq ss-xx 0)

(mapcar (lambda (ele) 
    (setq mean-x (+ mean-x (car ele)))
    (setq mean-y (+ mean-y (cdr ele)))
    (setq ss-xx (+ ss-xx (* (car ele) (car ele))))
    (setq ss-xy (+ ss-xy (* (car ele) (cdr ele))))
) linearData)

(setq mean-x (/ mean-x dataLen))
(setq mean-y (/ mean-y dataLen))
(setq ss-xx (- ss-xx (* dataLen (* mean-x mean-x ))))
(setq ss-xy (- ss-xy (* dataLen (* mean-x mean-y))))
(setq b-1 (/ ss-xy ss-xx))
(setq b-0 (- mean-y (* b-1 mean-x)))

(defun printem (&rest args)
  (format t "~{~a~^ ~}" args))
(print "______RESULT_______")
(print "")
(print (printem "LINEAR REGRESION IS: y =" (format nil "~f" b-0) "+(" (format nil "~f" b-1) "* x)"))

(let ((fileStream (open "newData.csv" :direction :output :if-exists :append )))
  (loop for a from 0 to 4
    do
    (setq new_5 (+ b-0 (* b-1 (+ dataLen a))))
    (setq ggtime (* (/ new_5 mean-y ) 100000))
    (if (< ggtime 0)(setq ggtime (* -1 ggtime)))
    (setq ggtime (round ggtime))
    (setq score (* ggtime new_5))
    (if (< score 0)(setq score (+ 2000 (* -1 score))))
    (if (< score 2000)(setq score (+ 2000 score)))
    (setq score (round score))
    (if (< new_5 1)(setq isWin 0)(setq isWin 1))
    (setq ans_row (list (+ dataLen a) isWin ggtime score))
    (cl-csv:write-csv-row ans_row :stream fileStream :always-quote nil )
    )   
(close fileStream))




