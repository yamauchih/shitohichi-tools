;; mi-mode.el --- mi file viewing mode.
;;
;; $Id:$
;;
;; Copyright (C) 2008-2011 Yamauchi, Hitoshi
;;
;; Author:     Yamauchi, Hitoshi <hyamauchi_at_nvidia.com>
;; Maintainer: Yamauchi, Hitoshi <hyamauchi_at_nvidia.com>
;; Last Updated: 2011-9-7(Wed)
;; Keywords: programming, elisp, mi scene descrition file
;;
;;------------------------------------------------------------
;; source location: /h/dev/scripts/emacs/mi-mode.el
;;------------------------------------------------------------
;;
;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either versions 2, or (at your option)
;; any later version.
;;
;; This program is distributed in the hope that it will be useful
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.
;;
;; Ref. http://www.emacswiki.org/cgi-bin/wiki/EasyFontLock
;;
;; Usage :
;;     1. Put this file to under the load-path.
;;     2. add next lines to your .emacs.
;;        (setq auto-mode-alist
;;              (append (list '("\\.mi$"  . mi-mode)
;;                            '("\\.mi2$" . mi-mode))
;;                       auto-mode-alist))
;;        (autoload 'mi-mode "mi-mode" "mi font lock mode" t)
;;
;; Customizing in your .emacs file.
;;
;; + When you want use font-lock (global effect),
;;
;;   - GNU Emacs   (global-font-lock-mode 1)
;;   - XEmacs      (font-lock-mode t)
;;
;;   font-lock only in mi-mode (local effect, Other mode follows
;;   global setting), add next lines to .emacs.
;;
;;     (add-hook 'mi-mode-hook
;;            (function (lambda ()
;;                        (and (boundp 'mi-mode-version-num)
;;                             (turn-on-font-lock)))))
;;
;;------------------------------------------------------------
;; (setq debug-on-error t)
;; (defun dbg (mes) (print mes (get-buffer "mi-debug")))
;;------------------------------------------------------------
;; mi-mode version
;;------------------------------------------------------------
(defconst mi-mode-version-num   "0.2.1"
  "The version of mi-mode.")
(defconst mi-mode-build-day     "2011-9-7(Wed)"
  "The build date of mi-mode.")

;;
;; show version
;;
(defun mi-mode-version ()
  "Print mi-mode version."
  (interactive)
  (cond ((interactive-p)
         (message "mi mode version %s of %s"
                  mi-mode-version-num mi-mode-build-day))))

;;------------------------------------------------------------
;; indentation setting
;;------------------------------------------------------------
;; (defvar mi-mode-indent-on t
;;   "* mi-mode indentation function is on.")
;; (make-variable-buffer-local 'mi-mode-indent-on)

;; (defvar mi-mode-tabs-start-offset 0
;;   "* mi-mode indentation tabs offset. The toplevel indentation starts with here")
;; (make-variable-buffer-local 'mi-mode-tabs-start-offset)

;; (defvar mi-mode-tabs-width 4
;;   "* mi-mode indentation tabs width.")
;; (make-variable-buffer-local 'mi-mode-tabs-width)

;; (defvar mi-mode-decrease-indent-level-with-brace-start t
;;   "* mi-mode indentation special case.
;; If the line starts with close bracket, the indent level is decreased.
;; e.g., when t
;;    add QIComboBox cbox=\"tri\" with { LABEL=\"primtype : \", RW=0,
;;      ITEMS=\"vtx tri edge\"
;;    };
;; e.g., when nil
;;    add QIComboBox cbox=\"tri\" with { LABEL=\"primtype : \", RW=0,
;;      ITEMS=\"vtx tri edge\"
;;         };")
;; (make-variable-buffer-local 'mi-mode-decrease-indent-level-with-brace-start)

;;------------------------------------------------------------
;; menu-bar
;;------------------------------------------------------------
(require 'easymenu)
(defvar mi-mode-menu-bar-map nil)
(defconst mi-mode-menu-spec
  '("mi-file"
    ;; ("Extract document"
    ;;  ["Get revised  document in manued buf"
    ;;   manued-show-newer-in-manued-buffer t]
    ;;  ["Get original document in manued buf"
    ;;   manued-show-older-in-manued-buffer t]
    ;;  ["Get revised  document from region"
    ;;   manued-show-newer-region	t]
    ;;  ["Get original document from region"
    ;;   manued-show-older-region	t])
    ;; "---"
    ["comment region"              	comment-region t]
    ["uncomment region"                 uncomment-region t]
    ["go to next declare"              	mi-mode-next-declare-keyword t]
    ["back to previous declare"         mi-mode-previous-declare-keyword t]
    ["Show version"          		mi-mode-version t]))

;;------------------------------------------------------------
;; syntax, abbrev tables
;;------------------------------------------------------------
(defvar mi-mode-syntax-table text-mode-syntax-table
  "* syntax table of mi-mode : default is `text-mode-syntax-table'")

(if mi-mode-syntax-table
    ()
  (setq mi-mode-syntax-table (make-syntax-table))
  (modify-syntax-entry ?#  "<" mi-mode-syntax-table)    ; comment start
  (modify-syntax-entry ?\n ">" mi-mode-syntax-table)    ; comment end
  )

(defvar mi-mode-abbrev-table text-mode-abbrev-table
  "* abbrev table of mi mode : default is `text-mode-abbrev-table'")


;; jump keyword
(defvar mi-mode-jump-keyword-regex
  "^end data\\|^data\\|^end declare\\|^declare\\|^end instance\\|^instance\\|^end instgroup\\|^instgroup\\|^end light\\|^light\\|^end lightprofile\\|^lightprofile\\|^end object\\|^object\\|^end options\\|^options\\|^end shader\\|^shader\\|^end trilist\\|^trilist"
  "Keyword to jump M-n and M-p"
  )

;;------------------------------------------------------------
;; font lock
;;------------------------------------------------------------
(defvar mi-mode-font-lock-keywords
  (list
   ;; for comments
   '("^[ \t]*#.*$"      0 'font-lock-comment-face)
   ;; for strings
   '("\"[^\"]*\""       0 'font-lock-string-face)
   ;; for declaration
   (cons (concat
          "\\<\\(?:"
          (regexp-opt
           '(
             "declare"
             "end"
             ))
          "\\|\\$\\(?:[0-9]+\\|\\sw+\\)\\)\\>")
         'font-lock-function-name-face)
   ;; for keyword name
   (cons (concat
          "\\<\\(?:"
          (regexp-opt
           '(
             "data"
             "default"
             "struct"
             "shader"
             "options"
             ))
          "\\|\\$\\(?:[0-9]+\\|\\sw+\\)\\)\\>")
         'font-lock-keyword-face)
   ;; variables?
   (cons (concat
          "\\<\\(?:"
          (regexp-opt
           '(
             "acceleration" "autovolume" "caustic" "colorclip" "contrast"
             "desaturate" "diagnostic" "samples" "displace" "dither" "face" "field"
             "filter" "finalgather" "gamma" "geometry" "globillum" "globillum"
             "globillum" "jitter" "lens" "luminance" "merge" "motion" "object"
             "output" "photon" "photonmap" "photonvol" "premultiply" "samples"
             "scanline" "shading" "shadow" "visible" "transparency" "transform"
             "material" "shadowmap" "shutter" "task" "time" "trace"
             ))
          "\\|\\$\\(?:[0-9]+\\|\\sw+\\)\\)\\>")
         'font-lock-variable-name-face)

   ;; constants?
   (cons (concat
          "\\<\\(?:"
          (regexp-opt
           '(
             "on" "off" "both" "size" "bsp2" "raw"
             ))
          "\\|\\$\\(?:[0-9]+\\|\\sw+\\)\\)\\>")
         'font-lock-constant-face)

   ;; mi expand keywords?
   (cons (concat
          "\\<\\(?:"
          (regexp-opt
           '(
             "boolean" "color" "scalar" "integer"
             ))
          "\\|\\$\\(?:[0-9]+\\|\\sw+\\)\\)\\>")
         'font-lock-type-face)
   ;; font-lock-doc-face
   ;; font-lock-warning-face
   )
  "Keyword highlighting specification for `mi-mode'.")


;;------------------------------------------------------------
;; indentation calculation
;;------------------------------------------------------------
;;
;; 1. start from current point
;; 2. find non-commented keyword "modify" (from the top when it is not
;;    found.)
;; 3. calculate the {} depth. But now I did not check the {} are in
;;    comment or not.
;;
;; (defun mi-mode-calculate-indentation-depth ()
;;   (save-excursion
;;     (beginning-of-line)
;;     (let ((current-point    0)
;;        (depth-of-bracket 0))
;;       (setq current-point (point))
;;       ;; if "modify" is found, goto there, else goto beginning of buffer.
;;       (if (re-search-backward "[^#].*modify" 0 t)
;;        (goto-char (match-beginning 0))
;;      (beginning-of-buffer))
;;       ;; find depth of the brackets
;;       (while (< (point) current-point)
;;      (progn
;;        (if (re-search-forward "\\({\\|}\\)" current-point t)
;;            (let ((found-str ""))
;;              (setq found-str
;;                    (buffer-substring (match-beginning 0) (match-end 0)))
;;              (cond ((string-equal found-str "{")
;;                     (setq depth-of-bracket (+ depth-of-bracket 1)))
;;                    ((string-equal found-str "}")
;;                     (setq depth-of-bracket (- depth-of-bracket 1)))
;;                    (t (error "Internal error"))))
;;          (goto-char current-point))))
;;       ;; if the this line starts with '}', then level is one less.
;;       (if mi-mode-decrease-indent-level-with-brace-start
;;        (progn
;;          (end-of-line)
;;          (let ((eol-point (point)))
;;            (beginning-of-line)
;;            ;; white space + } or } only. else {  } is matched.
;;            (if (re-search-forward "\\(^[ |\t^]+}\\|^}\\)" eol-point t)
;;                (setq depth-of-bracket (- depth-of-bracket 1))))
;;          ))
;;       depth-of-bracket)))

;; ;;
;; ;; calculate indentation.
;; ;;
;; (defun mi-mode-calculate-indentation ()
;;   "Return the column to which the current line should be indented."
;;   ;; (interactive)
;;   (+ mi-mode-tabs-start-offset
;;      (* mi-mode-tabs-width (mi-mode-calculate-indentation-depth))))

;; ;;
;; ;; indent the line.
;; ;;
;; (defun mi-mode-indent-line ()
;;   "Indent current line of mi-mode."
;;   (interactive)
;;   (let ((savep (> (current-column) (current-indentation)))
;;      (indent (condition-case nil (max (mi-mode-calculate-indentation) 0)
;;                (error "can not calculate indent?"))))
;;     (if savep
;;      (progn
;;        (dbg indent)
;;        (save-excursion (indent-line-to indent)))
;;       (indent-line-to indent))))

;;------------------------------------------------------------
;; moving funstions
;;------------------------------------------------------------
(defun mi-mode-next-declare-keyword (p)
  "goto next mi declare keyword"
  (interactive "d")
  (goto-char p)
  (let ((foundpos))
    (setq foundpos
          (re-search-forward
           mi-mode-jump-keyword-regex
           (point-max) t))
    (if (null foundpos)                 ; non exist
        (progn
          (message "mi-mode: no more next declare keyword.")
          (beep))
      (backward-char 1))))

(defun mi-mode-previous-declare-keyword (p)
  "goto previous mi declare keyword"
  (interactive "d")
  (goto-char p)
  (let ((foundpos))
    (setq foundpos
          (re-search-backward
           mi-mode-jump-keyword-regex
           (point-min) t))
    (if (null foundpos)                 ; non exist
        (progn
          (message "mi-mode: no more previous declare keyword.")
          (beep))
      (beginning-of-line))))


;;------------------------------------------------------------
;; keymap
;;------------------------------------------------------------
(defvar mi-mode-map nil
  "* keymap of mi.
\\<mi-mode-map>")

(progn
  (if (null mi-mode-map)
      (progn
        (setq mi-mode-map (make-sparse-keymap))
        ;;(define-key mi-mode-map "\t" 'mi-mode-indent-line)
        (define-key mi-mode-map "\M-n" 'mi-mode-next-declare-keyword)
        (define-key mi-mode-map "\M-p" 'mi-mode-previous-declare-keyword)
        ;; easy menu definition
        (easy-menu-define
          mi-mode-menu
          mi-mode-map
          "mi-mode: mental images scene description file format mode."
          mi-mode-menu-spec)
        )))

;;
;; mi mode
;;
(defun mi-mode ()
  "A major mode for editing mi files.
  - font lock high-lighting the keywords.
  - simple syntax based editing. (indent calculation, comment-region, etc.)

Special Commands:
\\<mi-mode-map>
"
  (interactive)
  (kill-all-local-variables)
  (use-local-map mi-mode-map)

  ;; mode
  (setq major-mode 'mi-mode)
  (setq mode-name "mi-mode")

  ;; syntax, abbrev table
  (set (make-local-variable 'comment-start) "# ")
  (set (make-local-variable 'comment-start-skip) "#+\\s-*")
  (set-syntax-table        mi-mode-syntax-table)
  (setq local-abbrev-table mi-mode-abbrev-table)

  (set (make-local-variable 'font-lock-defaults)
       '(mi-mode-font-lock-keywords t))
  (run-hooks 'mi-mode-hook)
  )

(provide 'mi-mode)

;;; mi-mode.el ends here
