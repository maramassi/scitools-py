DATA_PATH = "/data/18mia2_data/understand_results/data/"
REPO_PATH = "/data/18mia2_data/understand_results/subject_systems/"
GROUP_GENEALOGY_DISTINCT_PATH = "/data/18mia2_data/understand_results/data/group_genealogies_distinct"
UDB_PATH = "/data/18mia2_data/understand_results/data/udb"

GROUP_METRIC_PATH = '/data/18mia2_data/understand_results/data/group_metrics'
LABEL_PATH = '/data/18mia2_data/understand_results/data/label'

METRIC_COLUMNS = ["CountInput"
                 ,"CountLine"
                 ,"CountLineBlank"
                 ,"CountLineCode"
                 ,"CountLineCodeDecl"
                 ,"CountLineCodeExe"
                 ,"CountLineComment"
                 ,"CountOutput"
                 ,"CountPath"
                 ,"CountSemicolon"
                 ,"CountStmt"
                 ,"CountStmtDecl"
                 ,"CountStmtEmpty"
                 ,"CountStmtExe"
                 ,"Cyclomatic"
                 ,"CyclomaticModified"
                 ,"CyclomaticStrict"
                 ,"Essential"
                 ,"EssentialStrictModified"
                 ,"Knots"
                 ,"RatioCommentToCode"
                 ,"MaxEssentialKnots"
                 ,"MaxNesting"
                 ,"MinEssentialKnots"
                 ,"SumCyclomatic"
                 ,"SumCyclomaticModified"
                 ,"SumCyclomaticStrict"
                 ,"SumEssential"
                 ]

FEATURES = ['CountLine','CountLineComment','CountOutput','CountPath','CountInput', 'Essential','Knots','cnt_group_paras' ,'len_common_path' ,'cnt_distinct_contributors','cnt_group_followers','is_reusable']

ALL_FEATURES = ['CountLine', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe',
       'CountOutput', 'CountPath', 'CountSemicolon', 'CountStmt',
       'CountStmtDecl', 'CountStmtExe', 'Cyclomatic', 'CyclomaticModified',
       'CyclomaticStrict', 'Essential', 'SumCyclomatic',
       'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential',
       'CountInput', 'MaxNesting', 'CountLineBlank',
       'CountLineComment', 'Knots', 'RatioCommentToCode', 'MaxEssentialKnots',
       'MinEssentialKnots', 'cnt_group_paras', 'cnt_clone_siblings',
       'len_common_path', 'cnt_distinct_contributors', 'cnt_group_followers','is_reusable'
       ]
