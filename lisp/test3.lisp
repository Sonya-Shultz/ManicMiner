(setf my-array (make-array '(5 5) :initial-contents '((0 0 0 0 0) (0 0 0 0 0) (0 0 0 0 0) (0 0 0 0 0) (3 3 3 3 3))))
(setf (aref my-array 2 0) 1)
(setf (aref my-array 2 3) 2)
(setf (aref my-array 3 0) 3)
(setf (aref my-array 3 3) 3)
(print my-array)
(setf platforms (+ (random 2) 1))
(print platforms)
(dotimes (i platforms)
    (setf Len (+ (random 3) 1))
    (setf x (random 5))
    (setf y (random 5))
    
    (loop while (/= (aref my-array y x) 0) 
    do (setf x (random 5))
        (setf y (random 5)))
    (dotimes (j Len) 
        (if (< (+ x j) 5) (
            if (equal (aref my-array y (+ x j)) 0)(setf (aref my-array y (+ x j)) 3)
        ))
    )
)

(loop while (/= (aref my-array y x) 0) 
do (setf x (random 5))
    (setf y (random 5)))
(setf (aref my-array y x ) 4)
(loop while (/= (aref my-array y x) 0) 
do (setf x (random 5))
    (setf y (random 5)))
(setf (aref my-array y x ) 5)
(print my-array)

(defun score (data-arr depth user)
    (let ((dist 0)(key 0)(exit 0)(time-score depth)(key-c (list 0 0))(exit-c (list 0 0)))
        (dotimes (i 5)(dotimes (j 5)
            (if (equal (aref data-arr i j) 4)(setf key (+ key 1)))
            (cond ((equal (aref data-arr i j) 5)(setf exit (+ exit 1))(setf exit-c (list i j))))
        ))
        (setf dist-k 0)
        (setf dist 0)
        (if (< 0 key)
        (setf dist-k (sqrt (+ (* (- (car user) (car key-c))(- (car user) (car key-c))) (* (- (cadr user) (cadr key-c))(- (cadr user) (cadr key-c)))))))
        (if (< 0 exit)
        (setf dist (sqrt (+ (* (- (car user) (car exit-c))(- (car user) (car exit-c))) (* (- (cadr user) (cadr exit-c))(- (cadr user) (cadr exit-c)))))))
        (- (- (- 100 (+ time-score (+ key (* exit 10)))) (* dist 10))(* dist-k 7))
    )
)

(defun en-move (data-arr user)
    (let ((dist 0)(move-1 0)(move-2 0)(enemy-h (list 0 0))(enemy (list 0 0)))
        (dotimes (i 5)(dotimes (j 5)
            (if (equal (aref data-arr i j) 2)(setf enemy (list j i)))
        ))
        (setf enemy-h (copy-list enemy))
        (if (< (cadr enemy) (cadr user))(setf move-1 0)
            (if (< (cadr user) (cadr enemy))(setf move-1 3))
        )
        (if (< (car enemy) (car user))(setf move-2 1)
            (if (< (car user) (car enemy))(setf move-2 2))
        )
        (if (equal move-2 0)(setf move-2 move-1))
        (cond 
            ((equal 0 move-2)(setf (cadr enemy) (+ (cadr enemy) 1)))
            ((equal 1 move-2)(setf (car enemy) (- (car enemy) 1)))
            ((equal 2 move-2)(setf (car enemy) (+ (car enemy) 1)))
            ((equal 3 move-2)(setf (cadr enemy) (- (cadr enemy) 1)))
        )
        (cond 
            ((can_place_en? data-arr enemy)(setf (aref data-arr (cadr enemy-h) (car enemy-h)) 0)
            (setf (aref data-arr (cadr enemy) (car enemy)) 2))
        )

        (list move-2)

    )
)
(defun can_place_en? (data-arr user)
    (and (and ( and (and (< (car user) 5) (< (cadr user) 5)) (and (< -1 (car user)) (< -1 (cadr user))))(/= (aref my-array (cadr user) (car user)) 3))
    (and (/= (aref my-array (cadr user) (car user)) 4) (/= (aref my-array (cadr user) (car user)) 5)))
)
(defun can_place? (data-arr user)
    (and ( and (and (< (car user) 5) (< (cadr user) 5)) (and (< -1 (car user)) (< -1 (cadr user))))(/= (aref my-array (cadr user) (car user)) 3))
)

;0 - up 1-left 2-right 3-down

(defun do_move (data-arr move user-data)
    (let ((user (copy-list user-data)))
        (cond 
            ((equal 0 move)(setf (cadr user) (+ (cadr user) 1)))
            ((equal 1 move)(setf (car user) (- (car user) 1)))
            ((equal 2 move)(setf (car user) (+ (car user) 1)))
            ((equal 3 move)(setf (cadr user) (- (cadr user) 1)))
        )
        (cond((can_place? data-arr user)
            (if (equal (aref data-arr (cadr user) (car user)) 2)(setf (caddr user) (- (caddr user) 1)))
            (if (equal (aref data-arr (cadr user) (car user)) 4)(setf (aref data-arr (cadr user) (car user)) 0))
            (if (equal (aref data-arr (cadr user) (car user)) 5)(setf (aref data-arr (cadr user) (car user)) 0))
            (copy-list user))
            ((not (can_place? data-arr user))
            (copy-list user-data))
        )
    )

)

(defun copy-array (array &key
                (element-type (array-element-type array))
                (fill-pointer (and (array-has-fill-pointer-p array)
                    (fill-pointer array)))
                (adjustable (adjustable-array-p array)))
(let ((dims (array-dimensions array)))
    (adjust-array
    (make-array dims
        :element-type element-type :fill-pointer fill-pointer
        :adjustable adjustable :displaced-to array)
dims)))

(defun minimux (data-array depth user move user-data)
    (cond 
        ((> depth 2)
            (list nil (score data-array depth user-data))
        )
        ((equal user "user")
            (let ((b-score 0)(b-move -1)(h-score))
                (dotimes (i 4)
                    (let ((data-arr (copy-array data-array)))
                        (setf h-score (cadr (minimux data-arr depth "enemy" i (copy-list (do_move data-arr i user-data)))))
                        (cond ((< b-score h-score) (setf b-score h-score)(setf b-move i)))
                    )
                )
                (list b-move b-score)
            )
            
        )
        ((equal user "enemy")
            (minimux data-array (+ depth 1) "user" (car(en-move data-array user-data)) user-data)
        )
    )

)

(print (minimux my-array 0 "user" 0 (list 0 2 3)))

;(0 0 0 0 0)
;(0 0 0 0 0)
;(1 0 0 2 0)
;(3 0 0 3 0)
;(3 3 3 3 3)